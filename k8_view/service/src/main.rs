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
use std::thread;
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
pub fn write2chan(mut channel: Channel, chan: String, command: String) {
    let chan = "const".to_string(); //* 为以后多通道多终端预留 位置 */
    let lock = Arc::clone(&MESSAGEMAP);
    channel.exec(&command);
    loop {
        let mut buf = [0u8; 1000];
        match channel.read(&mut buf[..]) {
            Ok(n) => {
                println!("[{}]", n);
                if n == 0 {
                    break;
                }
                let mut result = String::new();
                let a = String::from_utf8_lossy(&buf[..n]);
                result.push_str(&a);
                let map = lock.lock();
                match map {
                    Ok(ref map) => match map.get(&chan) {
                        Some(chan) => {
                            chan.sed.clone().send(result);
                        }
                        _ => break,
                    },
                    Err(err) => break,
                }
            }
            Err(_) => break,
        }
    }
    channel.close();
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
pub async fn command(command: String, id: String, chan: String) -> String {
    let map = SESSIONMAP.clone();
    if let Ok(mut map) = map.lock() {
        if let Some(s) = map.get_mut(&id) {
            match s.channel_session() {
                //* 每条命令使用一条新的管道 */
                Ok(c) => {
                    thread::spawn(move || write2chan(c, chan, command));
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
