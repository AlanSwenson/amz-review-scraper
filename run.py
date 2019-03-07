from amz_review_scraper import create_app, db

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
