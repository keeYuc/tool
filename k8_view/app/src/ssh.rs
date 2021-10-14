use anyhow::{Context, Result};
use ssh2::{Channel, Session};
use std::net::TcpStream;
use std::path::Path;

pub fn connect(username: &str, addr: &str, port: i32, path: &str) -> Result<Session> {
    let tcp = TcpStream::connect(format!("{}:{}", addr, port))?;
    let mut sess = Session::new()?;
    sess.set_tcp_stream(tcp);
    sess.handshake()?;
    sess.userauth_pubkey_file(username, None, Path::new(path), None)?;
    Ok(sess)
}
