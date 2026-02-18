# Launch Kit

A CLI tool helping technical founders find users and validate their products.

## Features

- **Channel Analysis**: Analyze your product and get personalized channel recommendations (Reddit, Hacker News, Twitter, Product Hunt)
- **Content Generation**: Generate marketing copy templates optimized for each channel
- **Campaign Tracking**: Track your campaigns with metrics (clicks, conversions)

## Installation


## Usage

### Analyze Product & Get Channel Recommendations


This will prompt you for product details and recommend the best channels with scoring.

### Generate Content Templates


Creates channel-specific content templates (title, body, CTA).

### Create Campaign


Track a new marketing campaign with product name, channel, and post details.

### Update Campaign Metrics


### List All Campaigns


Filter by product:

## Example Workflow

1. Analyze your product to find best channels:
   ```bash
   python main.py analyze
   ```

2. Generate content for the top channel:
   ```bash
   python main.py generate-content
   ```

3. Post your content and create a campaign:
   ```bash
   python main.py create-campaign
   ```

4. Track results:
   ```bash
   python main.py update-metrics 1 --clicks 200 --conversions 10
   python main.py list-campaigns
   ```

## Database

Campaign data is stored in `launch_kit.db` (SQLite) in the current directory.