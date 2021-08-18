// use colored::Colorize;
use regex::Regex;
use std::io::{self, Read};
// use
use std::sync::mpsc;
use std::thread;


fn handle(str: String) -> String {
    let info = Regex::new("info").expect("regex info err");
    let error = Regex::new("error").expect("regex error err");
    let warn = Regex::new("warn").expect("regex warn err");
    let level = Regex::new("level").expect("regex level err");
    let msg = Regex::new("msg").expect("regex msg err");
    let caller = Regex::new("caller").expect("regex caller err");
    let a = info.replace_all(&str, "\x1B[0;32m info\x1B[0m");
    let a = warn.replace_all(a.as_ref(), "\x1B[0;35m warn\x1B[0m");
    let a = error.replace_all(a.as_ref(), "\x1B[0;31m error\x1B[0m");
    let a = level.replace_all(a.as_ref(), "\x1B[0;36m level\x1B[0m");
    let a = msg.replace_all(a.as_ref(), "\x1B[0;34m msg\x1B[0m");
    let a = caller.replace_all(a.as_ref(), "\x1B[0;33m caller\x1B[0m");
    return String::from(a);
}

fn main() {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || loop {
        let mut buf = String::new();
        io::stdin().read_line(&mut buf).expect("read err");
        tx.send(buf).expect("send err");
    });
    loop {
        match rx.recv() {
            Ok(a) => println!("{}", handle(a)),
            Err(err) => {
                println!("{}", err);
                break;
            }
        }
    }
    // for item in rx.recv() {
    //     println!("bbbbbbb");
    //     match item {
    //     }
    //     println!("{}", handle(item));
    //     println!("cccccccc");
    // }
}
