import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Snackbar,
  Alert,
} from '@mui/material';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-sql';
import 'ace-builds/src-noconflict/theme-github';
import axios from 'axios';

const NLToSQL = () => {
  const [description, setDescription] = useState('');
  const [dbEngine, setDbEngine] = useState('sqlite');
  const [sqlCode, setSqlCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [executionResults, setExecutionResults] = useState(null);

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleDbEngineChange = (e) => {
    setDbEngine(e.target.value);
  };

  const handleSqlChange = (newValue) => {
    setSqlCode(newValue);
  };

  const handleSubmit = async () => {
    if (!description.trim()) {
      setError('Please enter a database description');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/nl-to-sql', {
        text_description: description,
        db_engine: dbEngine
      });

      setSqlCode(response.data.sql_code);
      setSuccess(true);
    } catch (err) {
      setError(`Error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteSQL = async () => {
    if (!sqlCode.trim()) {
      setError('No SQL code to execute');
      return;
    }

    setExecuting(true);
    setError(null);

    try {
      const response = await axios.post('/api/execute-sql', {
        sql_code: sqlCode,
        db_engine: dbEngine
      });

      setExecutionResults(response.data);
      setSuccess(true);
    } catch (err) {
      setError(`Execution Error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setExecuting(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSuccess(false);
    setError(null);
  };

  return (
    <Container>
      <Box sx={{ pt: 4, pb: 8 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
          Natural Language to SQL
        </Typography>
        <Typography paragraph align="center" color="text.secondary" sx={{ mb: 6 }}>
          Describe your database structure in plain English and let our AI generate the SQL for you.
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Database Description
              </Typography>
              <TextField
                label="Describe your database"
                multiline
                rows={6}
                fullWidth
                variant="outlined"
                value={description}
                onChange={handleDescriptionChange}
                placeholder="Example: Create a database for a blog with users, posts, and comments. Users have a username, email, and password. Posts have a title, content, and timestamps. Comments have content and timestamps."
                sx={{ mb: 3 }}
              />

              <FormControl sx={{ minWidth: 200, mb: 3 }}>
                <InputLabel id="db-engine-label">Database Engine</InputLabel>
                <Select
                  labelId="db-engine-label"
                  value={dbEngine}
                  onChange={handleDbEngineChange}
                  label="Database Engine"
                >
                  <MenuItem value="sqlite">SQLite</MenuItem>
                  <MenuItem value="mysql">MySQL</MenuItem>
                  <MenuItem value="postgresql">PostgreSQL</MenuItem>
                </Select>
              </FormControl>

              <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                <Button
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={loading || !description.trim()}
                  startIcon={loading && <CircularProgress size={20} />}
                >
                  {loading ? 'Processing...' : 'Generate SQL'}
                </Button>
              </Box>
            </Paper>
          </Grid>

          {sqlCode && (
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Generated SQL
                </Typography>
                <Box sx={{ mb: 3 }}>
                  <AceEditor
                    mode="sql"
                    theme="github"
                    name="sql-editor"
                    value={sqlCode}
                    onChange={handleSqlChange}
                    editorProps={{ $blockScrolling: true }}
                    setOptions={{
                      showLineNumbers: true,
                      tabSize: 2,
                    }}
                    width="100%"
                    height="300px"
                  />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    variant="contained"
                    onClick={handleExecuteSQL}
                    disabled={executing || !sqlCode.trim()}
                    startIcon={executing && <CircularProgress size={20} />}
                  >
                    {executing ? 'Executing...' : 'Execute SQL'}
                  </Button>
                </Box>
              </Paper>
            </Grid>
          )}

          {executionResults && (
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Execution Results
                </Typography>
                {executionResults.error ? (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {executionResults.error}
                  </Alert>
                ) : (
                  <Alert severity="success" sx={{ mb: 2 }}>
                    SQL executed successfully
                  </Alert>
                )}
                {executionResults.execution_log && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Execution Log:
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 2, backgroundColor: '#f5f5f5' }}>
                      <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                        {executionResults.execution_log}
                      </pre>
                    </Paper>
                  </Box>
                )}
              </Paper>
            </Grid>
          )}
        </Grid>
      </Box>

      <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="error">
          {error}
        </Alert>
      </Snackbar>

      <Snackbar open={success} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="success">
          Operation completed successfully
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default NLToSQL; 