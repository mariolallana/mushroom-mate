import sys
import os
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn, TextColumn

# Add 'backend' directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params
from data_scripts.mushroom_probability_calculation import calculate_probabilities

# Setup rich logging and console
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt="[%X]",
    handlers=[RichHandler(console=console)]
)
logger = logging.getLogger("rich")

# Fetch location IDs and mushroom species using ForestModel
def fetch_data():
    with ForestModel(mysql_params) as db_model:
        locations = db_model.execute_query("SELECT location_id FROM forest WHERE tipo_id = 21")
        mushrooms = db_model.fetch_all_mushroom_species()
    return [loc['location_id'] for loc in locations], mushrooms

# Process a single location to calculate probabilities and prepare records
def process_location_batch(locations, mushrooms):
    results = []
    for location_id in locations:
        probabilities = calculate_probabilities(location_id)
        for prob_info in probabilities:
            if isinstance(prob_info, dict) and 'error' not in prob_info:
                specie_id = next((m['specie_id'] for m in mushrooms if m['specie_name'] == prob_info.get('specie_name')), None)
                if specie_id:
                    results.append((location_id, specie_id, prob_info.get('probability')))
    return results

# Update mushroom probabilities in the database
def update_probabilities(batch_size=100):
    locations, mushrooms = fetch_data()

    with ForestModel(mysql_params) as db_model:
        db_model.create_mushroom_probabilities_table()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Processing Locations...", total=len(locations))

            for i in range(0, len(locations), batch_size):
                batch = locations[i:i+batch_size]
                try:
                    results = process_location_batch(batch, mushrooms)
                    if results:
                        db_model.batch_update_probability_records(results)
                    progress.advance(task, len(batch))
                except Exception as e:
                    logger.error(f"[red]Error processing batch starting with location {batch[0] if batch else 'unknown'}: {str(e)}[/red]", exc_info=True)

    logger.info("[bold cyan]Mushroom probabilities update completed.[/bold cyan]")

# Print the first 10 records from the mushroom_probabilities table
def print_first_ten_probabilities():
    with ForestModel(mysql_params) as db_model:
        results = db_model.execute_query("SELECT * FROM mushroom_probabilities ORDER BY last_updated DESC LIMIT 10")
        console.print("[bold yellow]First 10 entries in mushroom_probabilities:[/bold yellow]")
        for row in results:
            console.print(row)

if __name__ == '__main__':
    try:
        update_probabilities()
        print_first_ten_probabilities()
    except Exception as e:
        logger.critical(f"[bold red]Critical error in main execution: {str(e)}[/bold red]", exc_info=True)
