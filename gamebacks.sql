CREATE OR REPLACE PROCEDURE users.add_review(
    p_game_id INT,
    p_user_id INT,
    p_rating INT,
    p_comment TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users.Reviews (GameID, UserID, Rating, Comment)
    VALUES (p_game_id, p_user_id, p_rating, p_comment);
END;
$$;
