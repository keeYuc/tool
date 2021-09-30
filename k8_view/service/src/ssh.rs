use anyhow::{Context, Result};
use ssh2::{Channel, Session};
use std::fs::OpenOptions;
use std::io::Read;
use std::net::TcpStream;
use std::path::Path;
const ADDR: &str = "10.1.151.159";
const PORT: i32 = 22;
const USERNAME: &str = "keeyu";
const PATH: &str = "/Users/keeyu/ssh/keeyu/id_rsa";
//---------------------------------------------------------------------------------------
#[test]
fn test_connect() -> Result<()> {
    let sess = connect_(USERNAME, ADDR, PORT, PATH)?;
    let mut channel = sess.channel_session()?;
    let str = do_command(&mut channel, "ls -a")?;
    println!("{}", str);
    Ok(())
}

pub fn do_command(c: &mut Channel, command: &str) -> Result<String> {
    let mut buf = String::new();
    c.exec(command)?;
    c.read_to_string(&mut buf)?;
    Ok(buf)
}

pub fn connect_(username: &str, addr: &str, port: i32, path: &str) -> Result<Session> {
    let tcp = TcpStream::connect(format!("{}:{}", addr, port))?;
    let mut sess = Session::new()?;
    sess.set_tcp_stream(tcp);
    sess.handshake()?;
    sess.userauth_pubkey_file(username, None, Path::new(path), None)?;
    Ok(sess)
}
