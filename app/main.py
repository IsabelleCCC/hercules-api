from fastapi import FastAPI
from api.routers.exercise import ExerciseRouter
from api.routers.user import UserRouter
from api.routers.workout_plan import WorkoutPlanRouter
from api.routers.fitness_test import FitnessTestRouter
from api.routers.exercise_workout_plan import ExerciseWorkoutPlanRouter
from api.routers.workout import WorkoutRouter
from api.routers.auth import AuthRouter

app = FastAPI()

app.include_router(AuthRouter)

app.include_router(ExerciseRouter)
app.include_router(UserRouter)
app.include_router(WorkoutPlanRouter)
app.include_router(FitnessTestRouter)
app.include_router(ExerciseWorkoutPlanRouter)
app.include_router(WorkoutRouter)
