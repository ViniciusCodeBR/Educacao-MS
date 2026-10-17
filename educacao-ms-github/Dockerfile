FROM maven:3.9.11-eclipse-temurin-21 AS build
WORKDIR /projeto
COPY pom.xml .
COPY src ./src
COPY gerados/carga.sql ./gerados/carga.sql
RUN mvn -B -DskipTests package

FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=build /projeto/target/educacao-ms-1.0.0.jar app.jar
ENV SERVER_ADDRESS=0.0.0.0
ENV JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=65.0"
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
