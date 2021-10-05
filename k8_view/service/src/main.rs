use anyhow::Result;
use ssh2::Channel;
use std::{
    borrow::BorrowMut,
    collections::HashMap,
    io::Read,
    sync::{Arc, Mutex},
};
mod data;
mod http;
mod ssh;
use http::{Rsb, SessionData};
use lazy_static::lazy_static;
use rocket::serde::json::Json;
use ssh::connect_;
use ssh2::Session;
use uuid::Uuid;
#[macro_use]
extern crate rocket;
////---------------------------------------------------------------------------------------
lazy_static! {
    static ref SESSIONMAP: Arc<Mutex<HashMap<String, Session>>> =
        Arc::new(Mutex::new(HashMap::new()));
    static ref MESSAGEMAP: Arc<Mutex<HashMap<String, data::message_chan>>> =
        Arc::new(Mutex::new(HashMap::new()));
}
////---------------------------------------------------------------------------------------
pub fn write2chan(chan: String, data: String) {
    let chan = "const".to_string(); //* 为以后多通道多终端预留 位置 */
    let lock = Arc::clone(&MESSAGEMAP);
    let map = lock.lock();
    match map {
        Ok(mut map) => match map.get_mut(&chan) {
            Some(chan) => {
                chan.sed.send(data);
            }
            _ => {
                println!("write2chan no chan");
                return;
            }
        },
        Err(err) => {
            println!("write2chan err:{}", err);
        }
    }
}
////---------------------------------------------------------------------------------------

#[get("/read?<chan>")]
pub async fn read(chan: String) -> Json<Rsb<String>> {
    let chan = "const".to_string(); //* 为以后多通道多终端预留 位置 */
    let lock = Arc::clone(&MESSAGEMAP);
    let map = lock.lock();
    match map {
        Ok(mut map) => match map.get_mut(&chan) {
            Some(chan) => {
                match chan.rcv.try_recv() {
                    Ok(str) => {
                        return Json(Rsb::ok(str));
                    }
                    Err(err) => {
                        return Json(Rsb::err(err.to_string()));
                    }
                };
            }
            _ => {
                return Json(Rsb::err("no chan".to_string()));
            }
        },
        Err(err) => {
            return Json(Rsb::err(err.to_string()));
        }
    }
}

#[get("/new-chan")]
pub async fn new_chan() -> Json<Rsb<String>> {
    let lock = Arc::clone(&MESSAGEMAP);
    let map = lock.lock();
    match map {
        Ok(mut map) => {
            let id = Uuid::new_v4().to_string();
            map.insert(id.clone(), data::message_chan::new());
            return Json(Rsb::ok(id));
        }
        Err(err) => {
            return Json(Rsb::err(err.to_string()));
        }
    }
}
fn init_chan() {
    let lock = Arc::clone(&MESSAGEMAP);
    let map = lock.lock();
    match map {
        Ok(mut map) => {
            let id = "const".to_string();
            map.insert(id.clone(), data::message_chan::new());
        }
        Err(err) => {
            println!("init err:{}", err);
            panic!();
        }
    }
}

#[get("/do_command?<command>&<id>&<chan>")]
pub async fn command(command: &str, id: String, chan: String) -> String {
    let map = SESSIONMAP.clone();
    if let Ok(mut map) = map.lock() {
        if let Some(s) = map.get_mut(&id) {
            match s.channel_session() {
                //* 每条命令使用一条新的管道 */
                Ok(ref mut c) => {
                    c.exec(command);
                    let mut buf = Vec::new();
                    let a = c.read(&mut buf);
                    println!("{:?}", a);
                    return "ok".to_string();
                }
                Err(err) => {
                    return err.to_string();
                }
            }
        } else {
            return "chan id err".to_string();
        }
    };
    "lock err".to_string()
}

#[post("/new-session", data = "<user_info>")]
pub async fn new_session(user_info: Json<SessionData<'_>>) -> Json<Rsb<String>> {
    match connect_(
        user_info.username,
        user_info.addr,
        user_info.port,
        user_info.key_path,
    ) {
        Ok(sess) => {
            let lock = Arc::clone(&SESSIONMAP);
            let map = lock.lock();
            match map {
                Ok(mut map) => {
                    let id = Uuid::new_v4().to_string();
                    map.insert(id.clone(), sess);
                    return Json(Rsb::ok(id));
                }
                Err(err) => {
                    return Json(Rsb::err(err.to_string()));
                }
            }
        }
        Err(err) => Json(Rsb::err(err.to_string())),
    }
}

#[launch]
fn rocket() -> _ {
    init_chan();
    rocket::build().mount("/", routes![new_session, command, new_chan, read])
}
