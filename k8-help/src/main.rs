extern crate clap;
use clap::{App, Arg};
use std::io::{self, Read};
use std::process::Command;

fn do_command(n: String, c: String, g: String) {
    let mut pod_command = format!("kubectl get pod -n {}", n);
    if g != String::new() {
        pod_command = format!("{}{}{}", pod_command, "|grep ", g)
    }
    println!("{}", pod_command);
    return;
    let a = Command::new("bash")
        .arg("-c")
        .arg(pod_command)
        //.arg("s")
        .output()
        .expect("failed to execute process")
        .stdout;
    println!("{:?}", String::from_utf8(a).unwrap())
}

fn main() {
    let matches = App::new("k8-quick")
        .version("1.0")
        .author("Keeyu<keeyucc@gmail.com>")
        .about("be happy")
        .arg(
            Arg::with_name("namespace")
                .short("n")
                .long("namespace")
                .value_name("NAMESPACE")
                .help("Sets a namespace for command")
                .takes_value(true),
        )
        .arg(
            Arg::with_name("container")
                .short("c")
                .long("container")
                .value_name("CONTAINER")
                .help("Sets a container for command")
                .takes_value(true),
        )
        .arg(
            Arg::with_name("grep")
                .short("g")
                .long("grep")
                .value_name("GREP")
                .help("just grep")
                .takes_value(true),
        )
        .get_matches();
    let mut n = "gcp".to_string();
    let mut c = "merchant".to_string();
    let mut g = String::new();
    if let Some(s) = matches.value_of("namespace") {
        n = String::from(s)
    }
    if let Some(s) = matches.value_of("container") {
        c = String::from(s)
    }
    if let Some(s) = matches.value_of("grep") {
        g = String::from(s)
    }
    do_command(n, c, g);
}

fn read_in() -> io::Result<()> {
    let mut buffer = String::new();
    let stdin = io::stdin(); // We get `Stdin` here.
    stdin.read_line(&mut buffer)?;
    Ok(())
}
