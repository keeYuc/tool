use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::{collections::HashMap, fs::OpenOptions, io::Read};
#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub users: HashMap<String, User>,
    pub commands: Commands,
}
#[derive(Debug, Default, Serialize, Deserialize)]
pub struct User {
    pub username: String,
    pub ip: String,
    pub port: String,
    pub path: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Commands {
    pub on_init: String,
}

impl Config {
    pub fn read() -> Result<Self> {
        let mut fd = OpenOptions::new().read(true).open("config.yaml")?;
        let mut buf = String::new();
        fd.read_to_string(&mut buf)?;
        let config: Self = serde_yaml::from_str(&buf)?;
        Ok(config)
    }
    pub fn add_user(
        &mut self,
        username: String,
        ip: String,
        port: String,
        path: String,
    ) -> Result<()> {
        self.users.insert(
            username.clone(),
            User {
                username: username,
                ip: ip,
                port: port,
                path: path,
            },
        );
        self.write()
    }
    fn write(&self) -> Result<()> {
        let mut fd = OpenOptions::new()
            .create(true)
            .write(true)
            .open("config.yaml")?;
        serde_yaml::to_writer(fd, self)?;
        Ok(())
    }
}
