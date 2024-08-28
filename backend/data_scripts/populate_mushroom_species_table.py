#import sqlite3
import mysql.connector
import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params 

mushroom_data = [
    (1, 'Boletus edulis', 'A popular edible mushroom, known as porcini. Porcini often grow in symbiosis with pine trees, especially in mountainous areas. The Pinar de pino albar has a high altitude range (846-2118m) which suits this mushroom\'s preferences.', 21, 25.0, 10.0, 600, 1000, 2000, 1000, 2200, 5, 'Highly prized for its rich, nutty flavor and meaty texture. Considered one of the best edible mushrooms.'),
    (2, 'Lactarius deliciosus', 'Commonly known as saffron milk cap or red pine mushroom. This species is commonly found in pine forests, particularly associated with Pinus sylvestris.', 21, 25.0, 5.0, 500, 800, 1800, 800, 2000, 4, 'Valued for its mild, slightly sweet taste and firm texture. Popular in Mediterranean cuisine.'),
    (3, 'Amanita caesarea', 'Known as Caesar\'s mushroom, prized in Roman cuisine. This species often grows in association with oak trees in Mediterranean climates. Encinares (Holm oak forests) are a suitable habitat.', 18, 30.0, 15.0, 600, 1000, 1400, 300, 1500, 5, 'Highly esteemed for its delicate flavor and tender texture. Considered a delicacy since ancient Roman times.'),
    (4, 'Cantharellus cibarius', 'Golden chanterelle, one of the most popular wild mushrooms. Chanterelles often grow in deciduous forests, particularly with oak species. Melojares provide a suitable habitat with a good altitude range.', 15, 25.0, 10.0, 700, 1200, 1700, 500, 2000, 5, 'Prized for its fruity, peppery flavor and aroma reminiscent of apricots. Widely used in gourmet cuisine.'),
    (5, 'Morchella esculenta', 'True morel, highly prized in culinary circles. Morels are often found in mixed deciduous forests, particularly in areas with ash trees. Fresnedas provide a suitable habitat.', 56, 20.0, 5.0, 500, 800, 1500, 300, 1800, 5, 'Highly sought after for its unique, nutty flavor and honeycomb texture. Considered a luxury ingredient in many cuisines.'),
    (6, 'Tricholoma matsutake', 'Matsutake mushroom, highly valued in Japanese cuisine. Matsutake mushrooms are strongly associated with pine forests, particularly Pinus sylvestris in Europe.', 21, 25.0, 8.0, 600, 1000, 1900, 1000, 2200, 5, 'Extremely prized in Japanese cuisine for its distinct spicy-aromatic odor and flavor. One of the most expensive mushrooms in the world.'),
    (7, 'Craterellus cornucopioides', 'Black trumpet or horn of plenty, known for its distinctive flavor. Black trumpets prefer mixed deciduous forests, often growing under oak or beech. This mixed forest type in the Mediterranean region is suitable.', 31, 22.0, 8.0, 800, 1300, 1600, 500, 1800, 4, 'Appreciated for its rich, smoky flavor and aroma. Often used in gourmet dishes and sauces.'),
    (8, 'Hydnum repandum', 'Wood hedgehog or sweet tooth, a popular edible mushroom. This species can be found in both coniferous and deciduous forests, making a mixed forest an ideal habitat.', 403, 23.0, 7.0, 700, 1100, 1700, 400, 2000, 3, 'Valued for its mild, slightly peppery taste and crunchy texture. Versatile in cooking.'),
    (9, 'Macrolepiota procera', 'Parasol mushroom, known for its large size and scaly cap. Parasol mushrooms often grow in open woodlands and grasslands. Dehesas, which are open woodland pastures, provide a suitable environment.', 34, 28.0, 12.0, 500, 900, 1500, 200, 1800, 4, 'Appreciated for its mild, nutty flavor and tender texture when cooked. Popular in European cuisine.'),
    (10, 'Pleurotus ostreatus', 'Oyster mushroom, widely cultivated and found in the wild. Oyster mushrooms grow on dead or dying hardwood trees. Riparian forests (Bosque ribereño) often contain a variety of hardwood species and provide the moisture these mushrooms prefer.', 33, 25.0, 5.0, 600, 1000, 1500, 0, 1800, 3, 'Valued for its mild, slightly sweet flavor and delicate texture. Widely used in various cuisines and as a meat substitute.'),
    (11, 'Agaricus campestris', 'Field mushroom, commonly found in grasslands and meadows. It prefers open areas with rich soil.', 34, 25.0, 10.0, 500, 800, 1200, 0, 1500, 3, 'Appreciated for its mild, earthy flavor. Often used as a substitute for cultivated button mushrooms.'),
    (12, 'Lactarius sanguifluus', 'Bloody milk cap, associated with pine forests in Mediterranean regions.', 24, 28.0, 12.0, 400, 700, 1600, 0, 1800, 3, 'Valued in Mediterranean cuisine for its mild, slightly sweet flavor. Often grilled or used in stews.'),
    (13, 'Russula cyanoxantha', 'Charcoal burner, found in deciduous and mixed forests, particularly with oak and beech trees.', 31, 24.0, 8.0, 600, 1000, 1800, 300, 2000, 3, 'Appreciated for its mild, nutty flavor and firm texture. Popular in European forest regions.'),
    (14, 'Amanita ponderosa', 'Spring Caesar, found in Mediterranean oak forests, particularly with Quercus ilex and Quercus suber.', 18, 26.0, 12.0, 500, 800, 1200, 200, 1400, 4, 'Highly valued in parts of Spain and Portugal for its delicate flavor and tender texture.'),
    (15, 'Boletus aereus', 'Dark cep or bronze bolete, associated with deciduous trees, especially oak and chestnut.', 31, 26.0, 12.0, 700, 1100, 1800, 400, 2000, 5, 'Highly prized for its intense, nutty flavor and firm texture. Often considered superior to Boletus edulis by some enthusiasts.'),
    (16, 'Lepista nuda', 'Wood blewit, found in various forest types and even in gardens.', 403, 20.0, 5.0, 600, 1000, 1600, 0, 1800, 3, 'Appreciated for its strong, woody aroma and mild, slightly peppery taste. Popular in French cuisine.'),
    (17, 'Calocybe gambosa', 'St. George\'s mushroom, found in grasslands and deciduous woodlands.', 34, 18.0, 5.0, 500, 800, 1400, 200, 1600, 4, 'Valued for its strong, mealy aroma and delicate flavor. Highly sought after in spring.'),
    (18, 'Tuber melanosporum', 'Périgord black truffle, grows underground in symbiosis with oak and hazel trees.', 18, 25.0, 5.0, 600, 900, 1500, 100, 1500, 5, 'Extremely prized for its intense, earthy aroma and flavor. One of the most expensive and sought-after culinary ingredients in the world.'),
    (19, 'Terfezia arenaria', 'Desert truffle, found in arid and semi-arid regions, associated with Helianthemum plants.', 7, 30.0, 15.0, 200, 500, 1000, 0, 1200, 4, 'Highly valued in North African and Middle Eastern cuisines for its subtle, nutty flavor. Often called the \'poor man\'s truffle\'.'),
    (20, 'Lactarius quieticolor', 'Oakbug milkcap, associated with pine forests, particularly Pinus pinaster.', 61, 26.0, 8.0, 500, 800, 1700, 0, 2000, 3, 'Appreciated for its mild, slightly peppery taste. Popular in some Mediterranean regions, especially in Spain.')
]

# References used:
#1. Boa, E. (2004). Wild edible fungi: A global overview of their use and importance to people. Food and Agriculture Organization of the United Nations.
#2. Hall, I. R., Lyon, A. J., Wang, Y., & Sinclair, L. (1998). Ectomycorrhizal fungi with edible fruiting bodies 2. Boletus edulis. Economic botany, 52(1), 44-56.
#3. Martínez-Peña, F., de-Miguel, S., Pukkala, T., Bonet, J. A., Ortega-Martínez, P., Aldea, J., & Martínez de Aragón, J. (2012). Yield models for ectomycorrhizal mushrooms in Pinus sylvestris forests with special focus on Boletus edulis and Lactarius group deliciosus. Forest Ecology and Management, 282, 63-69.
#4. Kuo, M. (2007). 100 edible mushrooms. University of Michigan Press.
#5. Moreno, G., Manjón, J. L., & Zugaza, A. (1986). La guía de Incafo de los hongos de la Península Ibérica. Incafo.
#6. Ortega, A., & Lorite, J. (2007). Macrofungi diversity in cork-oak and holm-oak forests in Andalucian "dehesas" (southern Spain); an efficient parameter for establishing priorities for its evaluation and conservation. Central European Journal of Biology, 2(2), 276-296.
#7. Oria de Rueda, J. A., Martín-Pinto, P., & Olaizola, J. (2008). Bolete productivity of cistaceous scrublands in northwestern Spain. Economic Botany, 62(3), 323-330.

def populate_mushroom_species_table():
    try:
        # Connect to the MySQL database
        db_model = ForestModel(mysql_params)
        print(f"Connected to database: {db_model.conn.database}")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return

    # Drop the existing mushroom_species table
    db_model.drop_mushroom_species_table()
    print("Dropped existing mushroom_species table.")

    # Recreate the mushroom_species table
    db_model.create_mushroom_species_table()
    print("Recreated mushroom_species table.")

    # Insert mushroom data into the mushroom_species table
    successful_insertions = 0
    for specie in mushroom_data:
        try:
            db_model.insert_mushroom_species(specie)
            print(f"Inserted mushroom species: {specie[1]}")
            successful_insertions += 1
        except mysql.connector.IntegrityError as e:
            print(f"Failed to insert {specie[1]} due to a UNIQUE constraint failure: {e}")
        except Exception as e:
            print(f"Failed to insert {specie[1]} due to an unexpected error: {e}")

    # Verify the number of inserted species
    total_species = len(mushroom_data)
    print(f"\nSuccessfully inserted {successful_insertions} out of {total_species} species.")
    
    if successful_insertions != total_species:
        print("Warning: Not all species were inserted successfully.")
    else:
        print("All species were inserted successfully.")

    # Verify each species in the database
    print("\nVerifying inserted species:")
    for specie in mushroom_data:
        try:
            result = db_model.fetch_mushroom_species_by_id(specie[0])
            if result:
                print(f"Verified: ID: {result['specie_id']}, Name: {result['specie_name']}")
            else:
                print(f"Warning: Species with ID {specie[0]} ({specie[1]}) not found in the database.")
        except Exception as e:
            print(f"Error verifying species with ID {specie[0]} ({specie[1]}): {str(e)}")

    print("\nRaw output of all mushroom species:")
    all_species = db_model.fetch_all_mushroom_species()
    for species in all_species:
        print(species)

    # Close the database connection
    try:
        db_model.conn.close()
        print("\nDatabase connection closed.")
    except Exception as e:
        print(f"\nFailed to close database connection: {e}")

if __name__ == '__main__':
    populate_mushroom_species_table()
