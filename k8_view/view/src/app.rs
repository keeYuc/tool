use yew::prelude::*;
pub struct App {
    link: ComponentLink<Self>,
    a:i32,
}

pub enum Msg {
    None,
    O(i32),
}


impl Component for App {
    type Message = Msg;
    type Properties = ();

    fn create(_: Self::Properties, link: ComponentLink<Self>) -> Self {
        App {link,a:0}
    }

    fn update(&mut self, _msg: Self::Message) -> ShouldRender {
        match _msg {
            Msg::None=>true,
            Msg::O(o)=>{self.a+=100;false},
        }
    }

    fn change(&mut self, _: Self::Properties) -> ShouldRender {
        false
    }

    fn view(&self) -> Html {
        html! {
            <div>
            <p>{ "Hello world!" }</p>
            <p>{self.a}</p>
            <button onclick=self.link.callback(|_| Msg::O(1))>
                        { "fuck" }
                    </button>
            <button onclick=self.link.callback(|_| Msg::None)>
                        { "fuck it" }
                    </button>
            </div>
        }
    }
}

