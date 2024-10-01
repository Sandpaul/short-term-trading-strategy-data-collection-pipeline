resource "aws_s3_bucket" "ingestion_bucket" {
    bucket = "ingestion-bucket-st-trading-strategy-data-collection-pipeline"
    object_lock_enabled = true
    lifecycle {
        prevent_destroy = true
    }
}
