use iced::{
    button, text_input::State, Align, Button, Column, Element, Length, Sandbox, Settings, Text,
    TextInput,
};
mod config;
mod ssh;
mod view;
pub fn main() -> iced::Result {
    App::run(Settings::default())
}

#[derive(Default)]
struct App {
    user: view::UserInput,
    tool: view::Tool,
}

#[derive(Debug, Clone)]
enum Message {
    UsernameInput(String),
    PathInput(String),
    IpInput(String),
    PortInput(String),
    UserSubmit,
    UserNew,
    UserShow,
}

impl Sandbox for App {
    type Message = Message;

    fn new() -> Self {
        let mut t = App::default();
        t.user.close = true;
        t
    }

    fn title(&self) -> String {
        String::from("App - Iced")
    }

    fn update(&mut self, message: Message) {
        match message {
            Message::UsernameInput(str) => self.user.username.value = str,
            Message::PathInput(str) => self.user.path.value = str,
            Message::PortInput(str) => self.user.port.value = str,
            Message::IpInput(str) => self.user.ip.value = str,
            Message::UserSubmit => {
                self.tool.close = false;
                self.user = view::UserInput::default();
                self.user.close = true;
            }
            Message::UserNew => {
                self.user.close = false;
                self.tool.close = true
            }
            Message::UserShow=>{
                
            }
        }
    }

    fn view(&mut self) -> Element<Message> {
        let mut app = Column::new().padding(20).align_items(Align::Center);
        if !self.user.close {
            app = app
                .push(
                    TextInput::new(
                        &mut self.user.username.state,
                        "username",
                        &self.user.username.value,
                        Message::UsernameInput,
                    )
                    .padding(10)
                    .width(Length::Units(200)),
                )
                .push(
                    TextInput::new(
                        &mut self.user.path.state,
                        "path",
                        &self.user.path.value,
                        Message::PathInput,
                    )
                    .padding(10)
                    .width(Length::Units(200)),
                )
                .push(
                    TextInput::new(
                        &mut self.user.ip.state,
                        "ip",
                        &self.user.ip.value,
                        Message::IpInput,
                    )
                    .padding(10)
                    .width(Length::Units(200)),
                )
                .push(
                    TextInput::new(
                        &mut self.user.port.state,
                        "port",
                        &self.user.port.value,
                        Message::PortInput,
                    )
                    .padding(10)
                    .width(Length::Units(200)),
                )
                .push(
                    button::Button::new(&mut self.user.button_state, Text::new("Add"))
                        .on_press(Message::UserSubmit)
                        .padding(10)
                        .width(Length::Units(220)),
                )
        }
        if !self.tool.close {
            app = app
                .push(
                    button::Button::new(&mut self.tool.new_user_state, Text::new("NewUser"))
                        .on_press(Message::UserNew)
                        .padding(10)
                        .width(Length::Units(220)),
                )
                .push(
                    button::Button::new(&mut self.tool.show_user_state, Text::new("ShowUser"))
                        .on_press(Message::UserShow)
                        .padding(10)
                        .width(Length::Units(220)),
                )
        }
        app.into()
    }
}
