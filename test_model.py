from ml_model.inference.predict import predict

sample = {
    "title": "Amazing Top 5 Tricks You Won’t Believe!",
    "description": "This video will shock you and change your life",
    "views": 500000,
    "likes": 20000,
    "comment_count": 3000,
    "category_id": 10
}

result = predict(sample)

print(result)