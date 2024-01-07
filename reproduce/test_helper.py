def run_test(client, create_statements, query_statements, message="This is a test:"):
    print(message)

    client.clear()

    try:
        client.batch_run(create_statements)
        print("Graph initialization done")
    except Exception as e:
        print("Graph initialization failed")
        print(str(e))

    for query in query_statements:
        print(f"Given query [{query}]:")
        try:
            print(client.run(query))
        except Exception as e:
            print(str(e))

    print("-----------------------------------------------")


def run_test_from_file(client, create_statements_file, query_statements, message="This is a test from file:"):
    create_statements = []
    with open(create_statements_file, 'r') as f:
        while True:
            statement = f.readline()
            if statement == '':
                break
            create_statements.append(statement)

    run_test(client, create_statements, query_statements, message=message)
