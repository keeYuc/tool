use rocket::serde::{Deserialize, Serialize};

#[derive(Deserialize, Debug)]
pub struct SessionData<'a> {
    pub username: &'a str,
    pub mode: &'a str,
    pub password: &'a str,
    pub addr: &'a str,
    pub key_path: &'a str,
    pub port: i32,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct Rsb<T> {
    pub code: i32,
    pub message: String,
    pub data: Option<T>,
}

impl<T> Rsb<T> {
    pub fn ok(t: T) -> Rsb<T> {
        Rsb {
            code: 200,
            message: "ok".to_string(),
            data: Some(t),
        }
    }
    pub fn err(str: String) -> Rsb<T> {
        Rsb {
            code: 200,
            message: str,
            data: None,
        }
    }
}
