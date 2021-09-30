use std::{
    borrow::BorrowMut,
    collections::HashMap,
    sync::{Arc, Mutex},
};

use anyhow::Result;
mod data;
mod http;
mod ssh;
use http::{Rsb, SessionData};
use lazy_static::lazy_static;
use rocket::serde::json::Json;
use ssh::{connect_, do_command};
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
fn write2chan(chan: String, data: String) -> Result<()> {
    // TODO
    Ok(())
}
////---------------------------------------------------------------------------------------

#[get("/index")]
pub async fn index() -> &'static str {
    "Hello, world!"
}

#[get("/read?<chan>")]
pub async fn read(chan: String) -> Json<Rsb<String>> {
    // TODO
    return Json(Rsb::ok(String::new()));
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

#[get("/do_command?<command>&<id>&<chan>")]
pub async fn command(command: &str, id: String, chan: String) -> String {
    let map = SESSIONMAP.clone();
    if let Ok(mut map) = map.lock() {
        if let Some(s) = map.get_mut(&id) {
            match s.channel_session() {
                Ok(ref mut c) => match do_command(c, command) {
                    Ok(str) => match write2chan(chan, str) {
                        Ok(_) => return "ok".to_string(),
                        Err(err) => return err.to_string(),
                    },
                    Err(err) => return err.to_string(),
                },
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
    rocket::build().mount("/", routes![index, new_session, command, new_chan, read])
}
