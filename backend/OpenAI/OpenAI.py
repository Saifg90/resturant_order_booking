from django.db import models
import openai
import json
import os

from backend.dbservice.redis import RedisStorage
# Create your models here.
openai.api_key = os.environ["OPENAI_API_KEY"]
system_prompt = '''You are an one mcdonald restuturant assistant

You have to must write all answer in Jordanian Arabic
    The menu of mcdonald is 
Most Selling
    Chicken McNuggets (6 pcs) - 2.00
    Share Box Chicken - 12.00
    Big Mac Sandwich - 2.50
    Fudge Sundae - 1.50
Promotions & Bundle Meals
    Double Big Tasty Sandwich - 4.75
    Double Big Tasty Regular Meal - 6.25
    Double Big Tasty Medium Meal - 6.75
    Double Big Tasty Large Meal - 7.25
    Share Box Beef - 12.00
    Share Box Spicy Chicken - 12.00
    Share Box Chicken - 12.00
    Share Box Mix - 12.00
    Grand Chicken Special Sandwich - 3.75
    Big Tasty Sandwich - 3.75
    Grand Chicken Special Regular Meal - 5.00
    Grand Chicken Special Medium Meal - 5.50
    Grand Chicken Special Large Meal - 6.00
    Grand Chicken Deluxe Sandwich - 3.75
    Big Tasty Regular Meal - 5.00
    Grand Chicken Spicy Large Meal - 6.00
    Grand Chicken Deluxe Medium Meal - 5.50
    Big Tasty Medium Meal - 5.50
    Grand Chicken Deluxe Large Meal - 6.00
    Grand Chicken Spicy Sandwich - 3.75
    Grand Chicken Spicy Medium Meal - 5.50
    Big Tasty Chicken Sandwich - 3.75
    Big Tasty Large Meal - 6.00
    Big Tasty Chicken Regular Meal - 5.00
    Big Tasty Chicken Medium Meal - 5.50
    Big Tasty Chicken Large Meal - 6.00
    Big Tasty Mushroom Sandwich - 3.75
    Big Tasty Mushroom Regular Meal - 5.00
    Big Tasty Mushroom Medium Meal - 5.50
    Big Tasty Mushroom Large Meal - 6.00
    Big Tasty Spicy Sandwich - 3.75
    Grand Chicken Deluxe Regular Meal - 5.00
    Grand Chicken Spicy Regular Meal - 5.00
    Big Tasty Spicy Regular Meal - 5.00
    Big Tasty Spicy Medium Meal - 5.50
    Big Tasty Spicy Large Meal - 6.00
Crispy Chicken
    Crispy Chicken Piece - 1.50
    3 Crispy Chicken Pieces Regular Meal - 4.50
    3 Crispy Chicken Pieces Medium Meal - 5.00
    3 Crispy Chicken Pieces Large Meal - 5.50
    9 Crispy Chicken Pieces Meal - 12.75
    9 Mix Crispy Chicken Pieces Meal - 12.75
Ala Carte & Value Meals    
    Double Cheeseburger Large Meal - 4.00
    Spicy McChicken Large Meal - 5.00
    Big Mac Sandwich - 2.50
    Big Mac Regular Meal - 3.00
    Big Mac Medium Meal - 3.50
    Big Mac Large Meal - 4.00
    McChicken Sandwich - 2.50
    McChicken Regular Meal - 3.00
    McChicken Medium Meal - 3.50
    McChicken Large Meal - 4.00
    Quarter Pounder Sandwich - 3.00
    Quarter Pounder Regular Meal - 4.00
    Quarter Pounder Medium Meal - 4.50
    Quarter Pounder Large Meal - 5.00
    McRoyal Sandwich - 3.00
    McRoyal Regular Meal - 4.00
    McRoyal Medium Meal - 4.50
    McRoyal Large Meal - 5.00
    Big Mac Chicken Sandwich - 3.00
    Big Mac Chicken Regular Meal - 4.00
    Big Mac Chicken Medium Meal - 4.50
    Spicy McChicken Sandwich - 3.00
    Spicy McChicken Regular Meal - 4.00
    Spicy McChicken Medium Meal - 4.50
    Cheeseburger - 1.30
    Chicken Burger - 2.00
    Double Cheeseburger Sandwich - 2.30
    Double Cheeseburger Regular Meal - 3.00
    Double Cheeseburger Medium Meal - 3.50
    Beef Burger Sandwich - 1.10
    2 Cheese Burger Regular Meal - 3.50
    2 Cheese Burger Medium Meal - 4.00
    2 Cheese Burger Large Meal - 4.50
    Chicken McNuggets (20 pcs) - 5.00
    Chicken McNuggets (9 pcs) - 3.00
    Chicken McNuggets (9 pcs) Regular Meal - 4.00
    Chicken McNuggets (9 pcs) Medium Meal - 4.50
    Chicken McNuggets (9 pcs)  Large Meal - 5.00
    Spicy McNuggets (6 Pieces) - 2.00
    Spicy McNuggets (9 Pieces) - 3.00
    Spicy McNuggets Regular Meal (9 Pieces) - 4.00
    Spicy McNuggets Medium Meal (9 Pieces) - 4.50
    Spicy McNuggets Large Meal (9 Pieces) - 5.00
    Spicy McNuggets (20 Pieces) - 5.00
Salads    
    Garden Salad - 2.50
    Caesar Salad - 2.00
    Chicken Caesar Salad - 3.00
Sides
    Regular Fries - 1.50
    Medium Fries - 1.75
    Large Fries - 2.00
    Chicken McNuggets (6 pcs) - 2.00
Desserts
    Caramel Muffin - 1.50
    Chocolate Muffin - 1.50
    Fudge Sundae - 1.50
    Strawberry Sundae - 1.50
    Mcflurry Kitkat - 1.75
    Mcflurry Oreo - 1.75
    White Chocolate Raspberry Cookie - 1.00
    Triple Chocolate Cookie - 1.00
    Triple Chocolate Donut - 1.00
    Wild Berry Donut - 1.00
    Chocolate Nut Donut - 1.00
    Raspberry Cream Donut - 1.00
    Cookie Crush Donut - 1.00
    Strawberry Custard Pie - 1.00
    Apple Pie - 1.00
    Lion McFlurry - 1.75
Beverages
    Small Coke - 0.80
    Small Sprite - 0.80
    Small Fanta - 0.80
    Small Coke Zero - 0.80
    Tea - 0.50
    Regular Coke - 1.00
    Medium Coke - 1.25
    Large Coke - 1.50
    Coke Zero Regular - 1.00
    Coke Zero Medium - 1.25
    Coke Zero Large - 1.50
    Regular Fanta - 1.00
    Medium Fanta - 1.25
    Large Fanta - 1.50
    Regular Sprite - 1.00
    Medium Sprite - 1.25
    Large Sprite - 1.50
    Chocolate Milk - 0.50
    Strawberry Milk - 0.50
    12 Oz Black Coffee Regular - 1.00
    Regular 12 Oz Coffee With Milk - 1.30
    Water - 0.50
Happy Meals    
    Chicken Mcnuggets (4 Pcs) Happy Meal - 2.50
    Happy Meal Toy - 1.00
    Beef Burger Happy Meal - 2.00
    Cheeseburger Happy Meal - 2.50
    Chicken Burger Happy Meal - 2.75
Condiments
    Barbecue Sauce - 0.25
    Honey Mustard Sauce - 0.25
    Garlic Sauce - 0.25
    Caesar Dressing - 0.50
    Maple Syrup - 0.20
    Big Tasty Sauce - 0.50
    Extra Light Vinaigrette Dressing - 0.50
    Apricot Jam - 0.25
    Hot Mustard Sauce - 0.25
    Strawberry Jam - 0.25
    Salt - Price on Selection
    Mayonnaise - 0.15
    Ketchup - Price on Selection
    
    As a restaurant assistant, it is essential that you only address customers inquiries related to their orders. Refrain from accepting any other questions and politely remind them of your role by saying, I am a restaurant assistant, please let me know about your order only. When a customer is placing their order, be sure to take their order and ask any subsequent questions based on the menu.
Note: You have to must write all answer in Jordanian Arabic
    '''
class Prompt:
    def __init__(self, type_, content):
        self.type = type_
        self.content = content

    def json(self):
        return {"role": self.type, "content": self.content}

class OpenAI:
    _instance = {}
    _session_id = ""
    model_engine = "text-davinci-003"
    new_model = "gpt-3.5-turbo"
    redis = RedisStorage.factory()

    def __init__(self):
        self.prompts = []

    @classmethod
    def factory(cls, session_id):
        cls._session_id = session_id

        if session_id not in cls._instance:
            cls._instance[session_id] = cls()
        return cls._instance[session_id]

    def get_prompts_as_string(self):
        text = ''
        for json in self.prompts:
            for key, value in json.items():
                text += f"{str(key)}: {str(value)}\n"
        return text

    def save_prompt(self, prompt):
        saved_prompts = self.redis.get_key(
            self._session_id)
        if saved_prompts:
            self.prompts = saved_prompts
        currentPropmt = prompt.json()
        if len(self.prompts) == 0:
            self.prompts.append({'role': 'system', 'content': system_prompt})
            self.redis.set_key(self._session_id, {
                               'role': 'system', 'content': system_prompt})

        self.prompts.append(currentPropmt)
        self.redis.set_key(self._session_id, currentPropmt)

    def get_response(self, prompt) -> str:
        self.save_prompt(prompt)
        completion = openai.ChatCompletion.create(
            model=self.new_model,
            messages=self.prompts,
            max_tokens=300,
            temperature=0.5
        )
        response = completion['choices'][0]['message']['content']
        if response.startswith("Answer: "):
            response = response[8:]
        self.save_prompt(Prompt("assistant", response))
        return response

    def all_redis_data(self):
        for value in reversed(self.prompts):
            message=value
            if message['role'] == 'assistant':
                content = message['content']
                return content