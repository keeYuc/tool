use anyhow::Result;
use mongodb::{bson::doc, options::ClientOptions, Client};
struct Mongo {
    database: Option<mongodb::Database>,
}

impl Mongo {
    async fn new<'a>(database: String) -> Mongo {
        let mut client_options = ClientOptions::parse("mongodb://localhost:27017")
            .await
            .unwrap();
        client_options.app_name = Some("Keeyu rust".to_string());
        if let Ok(client) = Client::with_options(client_options) {
            let db = client.database(&database);
            Mongo { database: Some(db) }
        } else {
            Mongo { database: None }
        }
    }
    async fn get_collection(
        &self,
        name: &str,
    ) -> Option<mongodb::Collection<mongodb::bson::Document>> {
        match self.database {
            Some(ref db) => Some(db.collection(name)),
            None => {
                println!("get db err");
                None
            }
        }
    }
}

#[tokio::main]
pub async fn main() -> Result<()> {
    let db = Mongo::new("rust_test".to_string()).await;
    if let Some(col) = db.get_collection("test").await {
        if let Ok(cursor) = col.find(doc! {"title":"1984"}, None).await {
            println!("{:?}", cursor);
        };
    };
    Ok(())
}
async fn test() {
    let docs = vec![
        doc! { "title": "1984", "author": "George Orwell" },
        doc! { "title": "Animal Farm", "author": "George Orwell" },
        doc! { "title": "The Great Gatsby", "author": "F. Scott Fitzgerald" },
    ];
}
