from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE `student_teacher` (
    `student_id` INT NOT NULL REFERENCES `student` (`id`) ON DELETE CASCADE,
    `teacher_id` INT NOT NULL REFERENCES `teacher` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `student_teacher`;"""
