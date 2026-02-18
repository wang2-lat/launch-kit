import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from typing import Optional
from datetime import datetime

from models import Product, Campaign, ChannelRecommendation
from database import Database
from analyzer import ProductAnalyzer
from templates import TemplateGenerator

app = typer.Typer(help="Launch Kit - Help technical founders find users and validate products")
console = Console()
db = Database()
analyzer = ProductAnalyzer()
template_gen = TemplateGenerator()


@app.command()
def analyze(
    name: str = typer.Option(..., prompt="Product name"),
    description: str = typer.Option(..., prompt="Product description"),
    target_audience: str = typer.Option(..., prompt="Target audience"),
    stage: str = typer.Option("mvp", prompt="Product stage (mvp/beta/launched)")
):
    """Analyze product and get channel recommendations"""
    product = Product(
        name=name,
        description=description,
        target_audience=target_audience,
        stage=stage
    )
    
    recommendations = analyzer.recommend_channels(product)
    
    console.print(f"\n[bold green]Analysis for {product.name}[/bold green]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Channel", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Reason")
    
    for rec in recommendations:
        table.add_row(rec.channel, f"{rec.score}/10", rec.reason)
    
    console.print(table)
    
    if typer.confirm("\nGenerate content templates for top channel?"):
        top_channel = recommendations[0].channel
        templates = template_gen.generate(product, top_channel)
        
        console.print(f"\n[bold yellow]Content Templates for {top_channel}[/bold yellow]\n")
        console.print(f"[bold]Title:[/bold] {templates['title']}")
        console.print(f"\n[bold]Body:[/bold]\n{templates['body']}")
        console.print(f"\n[bold]CTA:[/bold] {templates['cta']}")


@app.command()
def create_campaign(
    product_name: str = typer.Option(..., prompt="Product name"),
    channel: str = typer.Option(..., prompt="Channel (reddit/hn/twitter/producthunt)"),
    title: str = typer.Option(..., prompt="Post title"),
    url: Optional[str] = typer.Option(None, prompt="Post URL (optional)")
):
    """Create a new marketing campaign"""
    campaign = Campaign(
        product_name=product_name,
        channel=channel,
        title=title,
        url=url or "",
        posted_at=datetime.now()
    )
    
    campaign_id = db.save_campaign(campaign)
    console.print(f"[green]Campaign created with ID: {campaign_id}[/green]")


@app.command()
def update_metrics(
    campaign_id: int = typer.Argument(..., help="Campaign ID"),
    clicks: Optional[int] = typer.Option(None, help="Number of clicks"),
    conversions: Optional[int] = typer.Option(None, help="Number of conversions")
):
    """Update campaign metrics"""
    db.update_campaign_metrics(campaign_id, clicks, conversions)
    console.print(f"[green]Metrics updated for campaign {campaign_id}[/green]")


@app.command()
def list_campaigns(product_name: Optional[str] = typer.Option(None, help="Filter by product name")):
    """List all campaigns with metrics"""
    campaigns = db.get_campaigns(product_name)
    
    if not campaigns:
        console.print("[yellow]No campaigns found[/yellow]")
        return
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", justify="right")
    table.add_column("Product")
    table.add_column("Channel")
    table.add_column("Title")
    table.add_column("Clicks", justify="right")
    table.add_column("Conversions", justify="right")
    table.add_column("Posted")
    
    for c in campaigns:
        table.add_row(
            str(c.id),
            c.product_name,
            c.channel,
            c.title[:40] + "..." if len(c.title) > 40 else c.title,
            str(c.clicks or 0),
            str(c.conversions or 0),
            c.posted_at.strftime("%Y-%m-%d")
        )
    
    console.print(table)


@app.command()
def generate_content(
    product_name: str = typer.Option(..., prompt="Product name"),
    description: str = typer.Option(..., prompt="Product description"),
    channel: str = typer.Option(..., prompt="Channel (reddit/hn/twitter/producthunt)")
):
    """Generate content templates for a specific channel"""
    product = Product(
        name=product_name,
        description=description,
        target_audience="developers",
        stage="mvp"
    )
    
    templates = template_gen.generate(product, channel)
    
    console.print(f"\n[bold yellow]Content Templates for {channel}[/bold yellow]\n")
    console.print(f"[bold]Title:[/bold] {templates['title']}")
    console.print(f"\n[bold]Body:[/bold]\n{templates['body']}")
    console.print(f"\n[bold]CTA:[/bold] {templates['cta']}")


if __name__ == "__main__":
    app()
