import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts component mounted');
    console.log('Fetching from API endpoint:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Workouts API response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts data fetched:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts array:', workoutsData);
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return <div className="container mt-4"><p>Loading workouts...</p></div>;
  if (error) return <div className="container mt-4"><p>Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Workout Suggestions</h2>
      <div className="row">
        {workouts.length === 0 ? (
          <p>No workouts found.</p>
        ) : (
          workouts.map(workout => (
            <div key={workout.id} className="col-md-6 mb-3">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{workout.workout_name}</h5>
                  <p className="card-text">
                    <strong>Difficulty:</strong> {workout.difficulty}<br />
                    {workout.description && <><strong>Description:</strong> {workout.description}<br /></>}
                    {workout.exercises && (
                      <>
                        <strong>Exercises:</strong>
                        <ul>
                          {Array.isArray(workout.exercises) ? (
                            workout.exercises.map((exercise, idx) => (
                              <li key={idx}>{typeof exercise === 'string' ? exercise : exercise.name || JSON.stringify(exercise)}</li>
                            ))
                          ) : (
                            <li>{JSON.stringify(workout.exercises)}</li>
                          )}
                        </ul>
                      </>
                    )}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
export default Workouts;
