import random
from flask import Flask, render_template, request

# --- 1. CORE DATA STRUCTURES (SIMPLE LISTS) ---

class Car:
    """Class to represent a single car (Data Structure)."""
    def __init__(self, car_id, brand, model, daily_price, color):
        self.id = car_id
        self.brand = brand
        self.model = model
        self.daily_price = daily_price
        self.color = color
        self.is_available = True

# List to track all rental transactions (for profit calculation)
RENTAL_RECORDS = [] 

# --- 2. DATA GENERATION (60 Cars in a List) ---
CARS = []
BRANDS = {
    "Mercedes": (2022, 2025, 250, 350), 
    "BMW": (2021, 2024, 200, 300),
    "Audi": (2020, 2023, 180, 280),
    "Porsche": (2023, 2025, 350, 500)
}
COLORS = ["Red", "Blue", "Black", "White", "Grey", "Silver"]
car_id_counter = 1001 

for brand, (min_year, max_year, min_price, max_price) in BRANDS.items():
    for i in range(15): 
        model = random.randint(min_year, max_year)
        price = random.randint(min_price, max_price)
        color = random.choice(COLORS)
        CARS.append(Car(car_id_counter, brand, model, price, color))
        car_id_counter += 1

# --- 3. FLASK SETUP ---

app = Flask(__name__)

# --- 4. CORE LOGIC FUNCTIONS (LIST OPERATIONS) ---

def get_car_by_id(car_id):
    """Finds a car object by its ID from the CARS list."""
    # This is the simplest way to search a list in Python
    return next((car for car in CARS if car.id == car_id), None)

def calculate_profit():
    """Calculates the total profit from all rental records list."""
    return sum(record['cost'] for record in RENTAL_RECORDS)

def rent_car(car_id, days):
    """Logic for renting a car and recording the transaction."""
    car = get_car_by_id(car_id)
    
    if not car:
        return "Error: Car not found."
    if not car.is_available:
        return "Error: Car is currently rented."
    
    car.is_available = False # Change status in the list
    total_cost = car.daily_price * days
    
    # Record the profit in the RENTAL_RECORDS list
    RENTAL_RECORDS.append({
        'car_id': car_id,
        'days': days,
        'cost': total_cost
    })
    
    return f"Car {car_id} ({car.brand} {car.model}) rented successfully for {days} days. Total Cost: ${total_cost}"

def return_car(car_id):
    """Logic for returning a car."""
    car = get_car_by_id(car_id)
    
    if not car:
        return "Error: Car not found."
    if car.is_available:
        return "Error: Car is already available."
    
    car.is_available = True # Change status in the list
    return f"Car {car_id} ({car.brand}) returned successfully."

# --- 5. FLASK ROUTES ---

@app.route('/', methods=['GET'])
def index():
    """Displays the main page and handles car list filtering."""
    
    # Check for the availability filter in the URL
    show_available_only = request.args.get('available') == 'true'
    
    if show_available_only:
        # Filter the original CARS list
        filtered_cars = [car for car in CARS if car.is_available]
        message = "Displaying available cars only."
    else:
        filtered_cars = CARS
        message = "Welcome to Potato Car Rental 🥔."

    total_profit = calculate_profit()
    
    return render_template('index.html', 
                           cars=filtered_cars, 
                           profit=total_profit, 
                           message=message)

@app.route('/rent', methods=['POST'])
def rent_action():
    """Processes the car rental request."""
    total_profit = calculate_profit()
    try:
        car_id = int(request.form['car_id'])
        days = int(request.form['days'])
        
        result_message = rent_car(car_id, days)
        
        return render_template('index.html', cars=CARS, profit=calculate_profit(), message=result_message)
    except Exception as e:
        return render_template('index.html', cars=CARS, profit=total_profit, message=f"Error occurred: Please check the input and Car ID.")

@app.route('/return', methods=['POST'])
def return_action():
    """Processes the car return request."""
    total_profit = calculate_profit()
    try:
        car_id = int(request.form['car_id'])
        
        result_message = return_car(car_id)
        
        return render_template('index.html', cars=CARS, profit=calculate_profit(), message=result_message)
    except Exception as e:
        return render_template('index.html', cars=CARS, profit=total_profit, message=f"Error occurred: Please check the Car ID.")

if __name__ == '__main__':
    app.run(debug=True)