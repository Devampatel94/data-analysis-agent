# Cell 8: Main Agent Class
from src.resolve_column_index import resolve_column_indices
from src.ask_LLm import query_llama_maverick
from matplotlib import pyplot as plt
class DataAgent:
    def __init__(self):
        self.history = [{"role": "system", "content": "You're a smart data analyst. Answer all questions based on uploaded data.If they ask to summarize give copact expalnation about data. Also i am giving you image as text so dont reospond that this is not image data,analyse based on text only. "}]
        self.df = None
        self.text = None

    def load(self, content_type, data):
        if content_type == 'dataframe':
            self.df = data
            self.history.append({"role": "assistant", "content": f"Data loaded with shape {data.shape}, columns: {list(data.columns)}"})
        else:
            self.text = data  
            self.history.append({"role": "assistant", "content": "Text document loaded."})

    def ask(self, query):
        self.history.append({"role": "user", "content": query})

        # Visualization check
        if self.df is not None and any(word in query.lower() for word in ["plot", "graph", "chart", "visual"]):
            col_hints = resolve_column_indices(query, self.df)
            print(col_hints)
            if len(col_hints) >= 2:
                x_col, y_col = col_hints[0], col_hints[1]
                kind = "scatter"
            else:
                numeric = self.df.select_dtypes(include='number')
                if numeric.shape[1] < 2:
                    return "❌ Not enough numeric columns to plot.",None
                x_col, y_col = numeric.columns[:2]
                kind = "scatter"

            try:
                self.df.plot(x=x_col, y=y_col, kind=kind, title=f"{y_col} vs {x_col} ({kind})")
                print(col_hints)
                plt.grid()
                plt.show()
                return f"✅ Showing a {kind} plot of {y_col} vs {x_col}", plt.gcf()
            except Exception as e:
                return f"❌ Plot failed: {str(e)}"  


        # Add data context if necessary
        if self.df is not None:
            sample = self.df.head(3).to_string()
            self.history.append({"role": "assistant", "content": f"Sample data:\n{sample}"})
        elif self.text is not None:
            self.history.append({"role": "assistant", "content": self.text[:1500]})

        answer = query_llama_maverick(self.history)
        self.history.append({"role": "assistant", "content": answer})
        return answer,None
