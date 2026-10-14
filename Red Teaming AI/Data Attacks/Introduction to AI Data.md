
AI systems learn from data. Performance, reliability, and security all depend on it. When that data is wrong (corrupted, manipulated, or leaked) the model built on it inherits the problem, because it cannot tell the difference between legitimate patterns and patterns an attacker planted.

That single fact drives the entire threat landscape covered in this module.

To understand where attacks happen, we need to understand the normal flow first.

## The Data Pipeline: Fueling AI Systems

![Flowchart showing steps: Collect, Process, Transform, Utilize, leading to Utilization Targets: Train Models, Generate Predictions.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/the_data_pipeline.png)


## Data Collection

![Diagram of Data Sources feeding into Data Collection Stage, leading to Raw Diverse Data Stream/Files. Sources include Web App Logs, Transactional DBs, IoT Devices, Websites, Third Parties, and Other Sources.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/data_collection.png)

`Data collection` pulls raw information from wherever it originates. User interactions arrive from web applications as `JSON` logs streamed through `Apache Kafka`. Structured transaction records come out of `PostgreSQL`. IoT devices push sensor readings over `MQTT`, while web scrapers extract content from public sites and third parties deliver batch files. The data itself spans everything from `JPEG` images to complex semi-structured formats.

## Storage

![Diagram showing Raw Diverse Data flowing into Storage Layer with Storage Technologies: Relational DB, NoSQL DB, Data Lake, Time-Series DB, leading to Stored Assets: Datasets and Serialized Models.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/stor_age.png)

Where the data lands depends entirely on its shape. Structured records go into relational databases like `PostgreSQL`, while semi-structured logs fit better in `NoSQL` stores like `MongoDB`. Large, mixed datasets end up in massive `data lakes` built on distributed file systems or cloud object storage. Time-series data gets specialized tools like `InfluxDB`.


## Data Processing

![Diagram showing Data from Storage entering Data Processing & Transformation Stage with tasks: Cleaning, Scaling, Feature Engineering, Distributed Processing, Orchestration, leading to Prepared High-Quality Dataset.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/processing.png)

Raw data is almost never usable as-is. `Data processing and transformation` is the stage that turns it into something a model can learn from, and this is exactly where much of the actual engineering effort lives.

## Modeling

![Diagram showing Prepared High-Quality Dataset entering Analysis & Modeling Stage, with steps: Explore Data, Select Algorithm, Tune Hyperparameters, Validate Performance, leading to Trained & Validated Model.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/modeling.png)

Processed data feeds into the `analysis and modeling` stage. Data scientists explore the dataset in environments like `Jupyter Notebooks`, then train models with frameworks like `PyTorch` or `TensorFlow`. The cycle is highly iterative: pick an algorithm, tune `hyperparameters` with tools like `Optuna`, validate, adjust, and repeat. Cloud platforms bundle much of this lifecycle into managed environments to make it seamless.

## Monitoring and Maintenance

![Diagram showing Deployed Model in Production with Operational and ML Performance Monitoring, leading to Predictions, Feedback & New Data, and Retraining Pipeline, which updates the model.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/maintenance.png)

Deployed models do not stay static. `Monitoring and maintenance` tracks both standard operational health (like latency and throughput) and ML-specific metrics like `data drift` and prediction quality.

