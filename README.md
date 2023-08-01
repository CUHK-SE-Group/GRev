# Testing Graph Database Systems via Equivalent Query Rewriting

Features:

- Efficient Deployment: Initiate testing through Docker-compose for quick and streamlined server deployment.
- Comprehensive Monitoring: Detailed bug analysis is made possible through integration with Elastic Search and Kibana, ensuring consistent performance tracking.
- Real-Time Notifications: Configurable Lark webhooks provide instant test messages in your Instant Messaging (IM) app, keeping you informed on-the-go.
- Simplified Validation: Simply copy original queries to validate.py in Python to perform straightforward validation.

## Quick Start

### Prepare Queries

You need Java version 11 to run the GDsmith.

```
$ java --version                                                                                        
openjdk 11.0.19 2023-04-18
OpenJDK Runtime Environment (build 11.0.19+7-post-Ubuntu-0ubuntu122.04.1)
OpenJDK 64-Bit Server VM (build 11.0.19+7-post-Ubuntu-0ubuntu122.04.1, mixed mode, sharing)
```

Then run the `GDsmith.jar` in the `query_producer`. The following command will produce 100 files in `query_producer/logs/composite`. You can change the `num-thread` and `num-tries` to speed up the generation.

```
cd query_producer
java -jar GDsmith.jar --num-tries 100 --num-queries 5000 --algorithm compared3 --num-threads 16 composite
```


### Start Testing

Now you need to start the database servers. We have already provide the docker compose file, since Nebula requires a cluster, you have to start the Nebula cluster first.

```bash
$ cd nebula-docker-compose
$ docker compose up -d
```

Then go back to the project root, you just need to enter `docker compose up -d`, the testing will start.

```bash
$ docker compose up -d                                                                       
[+] Running 12/12
 ✔ Container elasticsearch                           Running                                             0.0s 
 ✔ Container pattern-transformer-cypher2gremlin-1    Running                                             0.0s 
 ✔ Container kibana                                  Running                                             0.0s 
 ✔ Container pattern-transformer-nebula_client-1     Running                                             0.0s 
 ✔ Container logstash                                Running                                             0.0s 
 ✔ Container pattern-transformer-tinkerpop_client-1  Started                                             0.8s 
 ✔ Container pattern-transformer-redis-stack-1       Ru...                                               0.0s 
 ✔ Container pattern-transformer-memgraph-1          Runni...                                            0.0s 
 ✔ Container pattern-transformer-redis_client-1      R...                                                0.0s 
 ✔ Container pattern-transformer-memgraph_client-1   Running                                             0.0s 
 ✔ Container pattern-transformer-neo4j-1             Running                                             0.0s 
 ✔ Container pattern-transformer-neo4j_client-1      R...                                                0.0s 
```

## Project Layout

```bash
├── configs                             # configurations
├── cypher                             # cyper generator
├── cypher2gremlin                     # an individual java project to transform cypher into gremlin
├── database_tests                     # main test logic controllers
├── db.json                            # a file that record the testing process
├── docker-compose.yaml                
├── Dockerfile
├── elk                                # elk toolkits for monitoring the testing process
├── evaluation                         # evaluations for paper
├── gdb_clients                        # client stubs for the GDB server.
├── logs                               # general logs, performance logs and logic bug log.
├── mutator                            # implementation of mutator
├── nebula-docker-compose              # an individual folder for establish the nebula database
├── query_file                          # a testing data dir
├── query_producer                     # a path that store the queries we used in the test
├── README.md
├── requirements.txt
├── scripts                            # scripts for quick start testing
└── webhook                            # webhooks for sending warning and error message to lark
```

The detailed testing procedure is archived in the `database_tests` directory. Let's delve deeper into its structure. Within `database_tests`, there are five subdirectories representing different databases: `memgraph`, `nebula`, `neo4j`, `redis`, and `tinkerpop`. As the testing procedures across these databases bear a lot of similarities, we've abstracted the overall process into a convenient script named `helper.py`. This allows for a uniform testing approach across different databases, improving efficiency and consistency.




```bash
├── helper.py
├── memgraph
│   ├── TestMemGraph.py
│   └── validator.py
├── nebula
│   ├── nebula.txt
│   ├── TestNebula.py
│   ├── test_nebula_simple.py
│   └── validator.py
├── neo4j
│   ├── TestNeo4j.py
│   └── validator.py
├── redis
│   ├── TestRedis.py
│   └── validator.py
└── tinkerpop
    ├── TestTinkerpop.py
    └── validator.py
```


In `helper.py`, we use `general_testing_procedure` to show the general proedures of metamorphic testing. Each distinct database only needs to pass the corresponding configurations into the `general_testing_procedure`.

Currently, we have the following configurable parameters:

- **Mode of Testing**: 
    - `live`: Sends messages directly to your Instant Messaging (IM) application.
    - `debug`: Runs local tests on a single file.
    - `normal`: Performs tests without sending messages to IM.
- **report**: Defines the IM reporting function and webhook token.
- **transform_times**: Sets the number of transformations to be carried out.
- **client**: Identifies the client for a given graph database.
- **logger**: Defines the logger.
- **source_file**: Specifies the input file that contains query clauses.
- **logic_inconsistency_trace_file**: Points to the logic bug output file.
- **database_name**: Indicates the name of the database.
- **mutator_func**: Sets the mutation strategy.
- **query_producer_func**: Defines the approach to handling the query file.
- **oracle_func**: Identifies the oracle.

```python
class TestConfig:
    def __init__(self, **kwargs):
        self.mode = kwargs.get('mode', 'live')
        self.report = kwargs.get('report', post)
        self.report_token = kwargs.get('report_token')
        self.transform_times = kwargs.get('transform_times', 5)

        self.client: GdbFactory = kwargs.get('client')
        self.logger: Logger = kwargs.get('logger')
        self.source_file = kwargs.get('source_file')
        self.logic_inconsistency_trace_file = kwargs.get('logic_inconsistency_trace_file')
        self.database_name = kwargs.get('database_name')

        self.mutator_func: Callable[[str], str] = kwargs.get('mutator_func', QueryTransformer().mutant_query_generator)
        self.query_producer_func = kwargs.get('query_producer_func', lambda: ([], []))
        self.oracle_func: Callable[[TestConfig, any, any], None] = kwargs.get("oracle_func")

        # temp val for consistency checker
        self.q1 = None
        self.q2 = None

        self.num_bug_triggering = 0
```