# 💪 hercules-api
This is a public repository that provides an API for the Hercules system. It allows users to perform various operations and retrieve information related to workouts, workout plans and physical assessment.

## About Hercules

Bodybuilding offers a wide range of benefits for the body and mind. However, tracking and recording your workouts can be a challenging and confusing task. This is what Hercules was created for,
providing a simple and effective solution to help you plan, record and monitor your bodybuilding workouts.

## Description
- The API was developed with Python (v3.10.9), using the FastAPI framework, SQL Alchemy ORM (Object-Relational Mapping) and Pydantic library for perform data validation. 
- The software architecture adopted is Clean Architecture focusing on Onion🧅, which is a design pattern in which the Software is developed in layers, each with its own
  concerns and responsibilities, where the outermost layers are abstractions of the innermost layers.

## Features

- API endpoints for data retrieval and manipulation
- Authentication and authorization mechanisms
- Login
- Workout plan
- Workout register
- Physical assessment
- User configs

## Installation

To set up the hercules-api project, follow these steps:

1. Clone the repository: `git clone https://github.com/IsabelleCCC/hercules-api.git`
2. Install the required dependencies: `pip install`
3. Configure the necessary environment variables (if any).
4. Start the server: `uvicorn main:app --reload`

## Usage

To use the hercules-api project, you can send HTTP requests to the provided API endpoints. The API documentation and examples can be found in the [docs](./docs) directory.

## Contributing

Contributions to the hercules-api project are welcome. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-new-feature`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request.

## License

The hercules-api project is licensed under the [MIT License](./LICENSE).

## Contact

If you have any questions or suggestions regarding the hercules-api project, please contact me at [isa.ccc@live.com](mailto:isa.ccc@live.com).

