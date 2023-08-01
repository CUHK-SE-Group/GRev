FROM maven:3.6.3-jdk-8-openj9 AS builder

WORKDIR /app

COPY . /app
RUN mvn clean package

FROM openjdk:8-jdk-alpine
WORKDIR /app
COPY --from=builder /app/target/demo-0.0.1-SNAPSHOT.jar .
CMD ["java", "-jar", "demo-0.0.1-SNAPSHOT.jar"]