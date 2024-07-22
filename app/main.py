from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.exercise import ExerciseRouter
from api.routers.user import UserRouter
from api.routers.workout_plan import WorkoutPlanRouter
from api.routers.workout_done import WorkoutDoneRouter
from api.routers.fitness_test import FitnessTestRouter
from api.routers.exercise_plan import ExercisePlanRouter
from api.routers.exercise_done import ExerciseDoneRouter
from api.routers.auth import AuthRouter

app = FastAPI()

# Replace with the origin(s) of your frontend
# origins = ['http://localhost:4200', 'http://10.0.2.2:4200']

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)


app.include_router(AuthRouter)

app.include_router(ExerciseRouter)
app.include_router(UserRouter)
app.include_router(WorkoutPlanRouter)
app.include_router(WorkoutDoneRouter)
app.include_router(FitnessTestRouter)
app.include_router(ExercisePlanRouter)
app.include_router(ExerciseDoneRouter)
