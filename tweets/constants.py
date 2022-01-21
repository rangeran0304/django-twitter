class TweetPhotoStatus:
    PENDING = 0
    APPROVED = 1
    REJECTED = 2

Tweet_Photo_Status_Choices = (
    (TweetPhotoStatus.PENDING,'pending'),
    (TweetPhotoStatus.REJECTED,'rejected'),
    (TweetPhotoStatus.APPROVED,'approved'),
)
TWEET_PHOTO_UPLOAD_limit = 9