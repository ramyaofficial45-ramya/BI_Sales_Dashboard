from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("dataset.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():

    # Total orders
    total_orders = int(len(df))

    # Revenue
    revenue = int((df['price'] * df['quantity']).sum())

    # Top product
    top_product = str(df['product'].mode()[0])

    # Category sales
    category_sales = df.groupby('category')['quantity'].sum().to_dict()
    category_sales = {str(k): int(v) for k, v in category_sales.items()}

    # City orders
    city_orders = df['city'].value_counts().to_dict()
    city_orders = {str(k): int(v) for k, v in city_orders.items()}

    # Monthly sales
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month

    monthly_sales = df.groupby('month')['quantity'].sum().to_dict()
    monthly_sales = {int(k): int(v) for k, v in monthly_sales.items()}

    return render_template("dashboard.html",
                           orders=total_orders,
                           revenue=revenue,
                           top_product=top_product,
                           category_sales=category_sales,
                           city_orders=city_orders,
                           monthly_sales=monthly_sales)

@app.route("/search", methods=["GET","POST"])
def search():
    result = None
    if request.method == "POST":
        try:
            order_id = int(request.form['order_id'])
            result = df[df['order_id']==order_id].to_dict(orient="records")
            if result:
                result = result[0]
        except:
            result = None
    return render_template("search.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
