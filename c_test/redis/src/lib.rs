mod redis;

#[no_mangle]
pub extern "C" fn redis() {
    redis::fetch_an_integer();
}
