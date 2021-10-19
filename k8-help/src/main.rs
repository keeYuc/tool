extern crate clap;

use clap::{App, Arg};

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

    // You can check the value provided by positional arguments, or option arguments
    if let Some(o) = matches.value_of("namespace") {
        println!("Value for namespace: {}", o);
    }

    if let Some(c) = matches.value_of("container") {
        println!("Value for container: {}", c);
    }
    if let Some(c) = matches.value_of("grep") {
        println!("Value for grep: {}", c);
    }
}
