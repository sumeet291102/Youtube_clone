## User Persona

- consumer
    - goals
        - watch tutorials and study
        - stay updated with latest trends and techonologies
        - watch entertainment videos
    - motivations
        - passion to learn and grow
        - curiosity to explore different programming languages, frameworks, and technologies
        - build a successful career in software engineering
    - challenges
        - finding high-quality educational content amidst the vast amount of videos on YouTube
        - manage time between watching educational videos and entertaining videos
    - every day activity
        - watch coding tutorial, tech talks, and interviews with software engineers
        - explore new programming languages, frameworks, and technologies

- creator
    - goals
        - share passion for coding and software development with others
        - build a community of like-minded individuals interested in learning to code
        - monetize YouTube channel through ads, sponsorships, and affiliate marketing
    - motivations
        - love for teaching and helping others learn complex concepts in a simple manner
        - potential to generate a passive income stream
    - challenges
        - creating engaging and informative content that stands out the crowd
        - growing subscriber base and increasing engagement on her videos
        - managing time effectively between creating content, promoting channel, and personal commitments
    - every day activity
        - plan and scripts coding tutorials, focusing on beginner-friendly topics and advanced concepts
        - record, edit, and upload videos
        - engages with audience through comments, Q&A sessions, and live streams

## user stories

- consumer
    - isbat consume a wide range of programming-related content, including tutorials, lectures, and tech talks.
    - isbat easily search for videos on specific topics or technologies relevant to my studies.
    - isbat save videos to a watchlist or playlist for future reference.

- creator
    - isbat create and upload videos on programming topics that I am passionate about.
    - isbat edit my videos to ensure they are engaging and informative.
    - isbat promote my videos to reach a wider audience and receive feedback from viewers.
    - isbat get analytics to track the performance of my videos and audience engagement.

## database schema

- Users Table:
  - id (Primary Key)
  - username
  - email
  - password_hash
  - created_at

- Videos Table:
  - id (Primary Key)
  - title
  - description
  - url
  - user_id (Foreign Key to Users Table)
  - created_at

- Comments Table
  - id (Primary Key)
  - video_id (Foreign Key to Videos Table)
  - user_id (Foreign Key to Users Table)
  - content
  - created_at

- Likes Table
  - id (Primary Key)
  - video_id (Foreign Key to Videos Table)
  - user_id (Foreign Key to Users Table)
  - created_at

- Subscriptions Table (For User Subscriptions)
  - id (Primary Key)
  - subscriber_id (Foreign Key to Users Table)
  - channel_id (Foreign Key to Users Table)
  - created_at
