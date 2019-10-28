def getAction(rgb, paddlA, paddleB, ball, reward, done):
    paddle_y = paddlA.y
    ball_y = ball.y

    return -5 if paddle_y < ball_y else 5 if paddle_y > ball_y else 0
