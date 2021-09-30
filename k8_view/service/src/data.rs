use std::sync::mpsc::{self, channel};
pub struct message_chan {
    pub rcv: mpsc::Receiver<String>,
    pub sed: mpsc::Sender<String>,
}

impl message_chan {
    pub fn new() -> Self {
        let (sed, rcv) = channel::<String>();
        message_chan { rcv, sed }
    }
}
