use iced::{
    button, text_input::State, Align, Button, Column, Element, Length, Sandbox, Settings, Text,
    TextInput,
};
//------------------------------------------------------------------------------------------------------------------
#[derive(Debug, Clone, Default)]
pub struct UserInput {
    pub username: Input_,
    pub path: Input_,
    pub port: Input_,
    pub ip: Input_,
    pub button_state: button::State,
    pub close: bool,
}

#[derive(Debug, Clone, Default)]
pub struct Input_ {
    pub value: String,
    pub state: State,
}

//------------------------------------------------------------------------------------------------------------------
#[derive(Debug, Clone, Default)]
pub struct Tool {
    pub new_user_state: button::State,
    pub show_user_state: button::State,
    pub close: bool,
}

//------------------------------------------------------------------------------------------------------------------
