from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded!"

        try:
            df = pd.read_csv(file)
            numeric_summary_df = df.describe()
            friendly_numeric = {}
            for col in numeric_summary_df.columns:
                friendly_numeric[col] = {
                    'Average': round(numeric_summary_df[col]['mean'], 2),
                    'Minimum': numeric_summary_df[col]['min'],
                    'Maximum': numeric_summary_df[col]['max'],
                    'Median': numeric_summary_df[col]['50%'],
                    'Variation': round(numeric_summary_df[col]['std'], 2)
                }
            categorical_summary = {}
            for col in df.columns:
                unique_vals = df[col].unique()
                categorical_summary[col] = {
                    'Unique Count': len(unique_vals),
                    'Values': ", ".join(map(str, unique_vals))
                }

            return render_template(
                'index.html',
                friendly_numeric=friendly_numeric,
                categorical_summary=categorical_summary
            )

        except Exception as e:
            return f"Error reading CSV: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
