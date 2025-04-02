FROM maven:3.8.5-openjdk-17-slim AS build

WORKDIR /app

# ✅ Copy everything together to avoid caching old source code
COPY . .

# 🔄 Clean & rebuild the entire project
RUN mvn clean package -DskipTests

FROM openjdk:17-jdk-slim

WORKDIR /app

COPY --from=build /app/target/UserService-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 8081

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
