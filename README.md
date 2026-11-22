# &#x20;**E-Commerce Customer Behavior \& Revenue Analytics**

##### 

##### An end-to-end data analytics and machine learning project that transforms e-commerce transaction data into actionable business insights using Python, PostgreSQL, dbt, Power BI, Machine Learning, and a locally hosted AI business analyst.

##### 

## &#x20;**Project Overview**

##### 

##### This project analyzes customer purchasing behavior, product performance, revenue trends, and customer retention. It also incorporates machine learning models and a natural-language AI analyst that generates and executes validated SQL queries against a read-only PostgreSQL account.

##### 

## &#x20;**Technology Stack**

##### 

##### | Area | Technologies |

##### |---|---|

##### | Programming | Python, SQL |

##### | Data Analysis | Pandas, NumPy, Matplotlib |

##### | Database | PostgreSQL |

##### | Data Transformation | dbt |

##### | Business Intelligence | Power BI |

##### | Machine Learning | Scikit-learn |

##### | AI Integration | Ollama, Qwen 3 4B |

##### | AI Application | Streamlit |

##### | SQL Validation | SQLGlot |

##### | Version Control | Git, GitHub |

##### 

## &#x20;**## Project Architecture**

## 

##### ```text

##### &#x20;                Raw E-Commerce Data

##### &#x20;                         |

##### &#x20;                         v

##### &#x20;                  Python \& Pandas

##### &#x20;                (Data Cleaning and EDA)

##### &#x20;                         |

##### &#x20;                         v

##### &#x20;                    PostgreSQL

##### &#x20;                   (Data Storage)

##### &#x20;                         |

##### &#x20;                         v

##### &#x20;                        dbt

##### &#x20;            (Staging, Intermediate, Marts)

##### &#x20;                         |

##### &#x20;             +-----------+-----------+

##### &#x20;             |                       |

##### &#x20;             v                       v

##### &#x20;          Power BI              Machine Learning

##### &#x20;         (Dashboards)          (Segmentation,

##### &#x20;                               Prediction,

##### &#x20;                               Forecasting)

##### &#x20;                                     |

##### &#x20;                                     v

##### &#x20;                             AI Business Analyst

##### &#x20;                               (Ollama + Qwen 3)

##### &#x20;                                     |

##### &#x20;                                     v

##### &#x20;                               SQL Validation

##### &#x20;                                     |

##### &#x20;                                     v

##### &#x20;                                 PostgreSQL

##### &#x20;                              (Read-only Access)

##### &#x20;                                     |

##### &#x20;                                     v

##### &#x20;                              Business Insights

##### ```

## &#x20;**Business Analysis**

##### 

### The project explores:

##### 

##### \- Customer purchasing behavior and repeat purchases.

##### \- Customer segmentation using RFM analysis and K-Means clustering.

##### \- Product and category performance.

##### \- Monthly revenue and profitability trends.

##### \- Payment success and refund patterns.

##### \- Customer retention and cohort analysis.

##### 

## &#x20;**Key Business Findings**

##### 

##### | Metric | Result |

##### |---|---:|

##### | Total Customers | 20,000 |

##### | Total Orders | 100,000 |

##### | Purchasing Customers | 19,850 |

##### | Repeat Customers | 19,017 |

##### | Repeat Purchase Rate | 95.8% |

##### | Gross Order Revenue | $63.46M |

##### | Net Collections After Refunds | $60.07M |

##### | Gross Product Profit | $29.60M |

##### | Gross Product Margin | 50.40% |

##### 

##### \***Note**: Gross order revenue, product revenue, gross product profit, and net collections are different financial measures.\*

##### 

## &#x20;**Machine Learning**

##### 

##### Three machine learning tasks were explored:

##### 

##### 1\. \*\*Customer Segmentation:\*\* K-Means clustering to identify High Value Frequent, Regular, and At Risk customer groups.

##### 2\. \*\*Repeat Purchase Prediction:\*\* Classification models to explore which customer characteristics relate to repeat purchasing.

##### 3\. \*\*Revenue Forecasting:\*\* Time-series analysis and forecasting of monthly revenue.

##### 

##### The repeat-purchase classification experiments showed limited predictive signal, making this an important model evaluation finding rather than a result to overstate.

##### 

## &#x20;**AI Business Analyst**

##### 

##### The project includes a local AI-powered analytics assistant built using:

##### 

##### \- Ollama

##### \- Qwen 3 4B

##### \- PostgreSQL

##### \- SQLGlot

##### \- Streamlit

##### 

##### Users can ask business questions in natural language. The application:

##### 

##### 1\. Converts the question into SQL.

##### 2\. Validates the generated SQL against safety rules.

##### 3\. Executes permitted queries using a read-only database account.

##### 4\. Returns the query results.

##### 5\. Uses the local LLM to explain the findings.

##### 

##### The AI assistant currently uses an allowlist of approved analytics tables and restricted SQL operations.

##### 

## &#x20;**Power BI Dashboard**

##### 

##### The Power BI reports cover:

##### 

##### \- Product Performance

##### \- Customer Analytics

##### \- Revenue \& Financial Analytics

##### 

##### Dashboard screenshots will be added here.

##### 

## &#x20;**Project Structure**

##### 

##### ```text

##### ecommerce\_customer\_analytics/

##### |

##### ├── agents/

##### │   ├── ai\_business\_analyst.py

##### │   ├── streamlit\_app.py

##### │   ├── generate\_sql.py

##### │   ├── validate\_sql.py

##### │   └── ...

##### |

##### ├── ecommerce\_analytics\_dbt/

##### │   ├── models/

##### │   │   ├── staging/

##### │   │   ├── intermediate/

##### │   │   └── marts/

##### │   └── dbt\_project.yml

##### |

##### ├── notebooks/

##### │   ├── 01\_data\_exploration.ipynb

##### │   └── 01\_ml\_data\_preparation.ipynb

##### |

##### ├── sql/

##### │   └── 01\_database\_setup.sql

##### |

##### ├── requirements.txt

##### └── README.md

##### ```

##### 

## &#x20;**Running the Project Locally**

##### 

#### &#x20;**1. Clone the repository**

##### 

##### ```bash

##### git clone https://github.com/Ayush07-sys/E-Commerce-Customer-and-Analytics.git

##### cd E-Commerce-Customer-and-Analytics

##### ```

##### 

#### &#x20;**2. Create and activate a virtual environment**

##### 

##### ```bash

##### python -m venv .venv

##### ```

##### 

##### Windows:

##### 

##### ```cmd

##### .venv\\Scripts\\activate

##### ```

##### 

#### &#x20;**3. Install dependencies**

##### 

##### ```bash

##### pip install -r requirements.txt

##### ```

##### 

#### &#x20;**4. Configure PostgreSQL and dbt**

##### 

##### \- Install and start PostgreSQL.

##### \- Obtain and load the source dataset into the `staging` schema.

##### \- Configure your dbt profile locally.

##### \- Run dbt models and tests.

##### 

##### ```bash

##### cd ecommerce\_analytics\_dbt

##### dbt run

##### dbt test

##### ```

##### 

#### &#x20;**5. Run the local AI application**

##### 

##### Install Ollama and download the model:

##### 

##### ```bash

##### ollama pull qwen3:4b

##### ```

##### 

##### Configure the PostgreSQL connection and the read-only `ai\_analyst` user locally.

##### 

##### From the project root, launch:

##### 

##### ```bash

##### streamlit run agents/streamlit\_app.py

##### ```

##### 

## &#x20;**Data \& Security**

##### 

##### \- Raw datasets and processed data are not included in this repository.

##### \- Database credentials and API keys should be configured locally and must never be committed.

##### \- The AI analyst uses a restricted read-only PostgreSQL account.

##### \- The local AI application requires PostgreSQL and Ollama to be running.

##### 

## &#x20;**Future Improvements**

##### 

##### \- Public Streamlit demo deployment.

##### \- Additional dashboard screenshots and documentation.

##### \- Improved predictive model performance.

##### \- Automated data pipelines.

##### \- Advanced AI analytics and agentic workflows.

##### 

## &#x20;**Author**

##### 

##### \*\*Ayush Kumar\*\*

##### 

##### B.Tech — Artificial Intelligence \& Data Science

##### 

##### \[GitHub Profile](https://github.com/Ayush07-sys)

##### 

##### \---

##### 

##### \*This project was developed as an end-to-end portfolio project to demonstrate practical skills in data analytics, data engineering, business intelligence, machine learning, and AI integration.\*

