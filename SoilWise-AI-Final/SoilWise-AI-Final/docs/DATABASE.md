# Database Schema (implemented)

## users
- `id` UUID-like string primary key
- `email` unique and indexed
- `password_hash`, `full_name`, `preferred_language`, `created_at`

## analyses
- `id` UUID-like string primary key
- `user_id` foreign key to users, indexed
- `field_name`, optional `image_path`
- `nitrogen`, `phosphorus`, `potassium`, `ph`, `organic_matter`, `moisture`
- `health_score`, JSON `diagnosis`, JSON `recommendations`, `created_at`
- composite index on `(user_id, created_at)`

All analysis reads are scoped to the authenticated user. N/P/K are currently assumed to be mg/kg; this must match the source lab method before operational use. Field entity normalization is a future migration, not part of this schema.
