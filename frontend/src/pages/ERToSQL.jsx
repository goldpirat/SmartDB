import React, { useState, useCallback } from 'react';
import {
  Box,
  Container,
  Typography,
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
import { useDropzone } from 'react-dropzone';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-sql';
import 'ace-builds/src-noconflict/theme-github';
import axios from 'axios';

const ERToSQL = () => {
  const [file, setFile] = useState(null);
  const [dbEngine, setDbEngine] = useState('sqlite');
  const [sqlCode, setSqlCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [executionResults, setExecutionResults] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleDbEngineChange = (e) => {
    setDbEngine(e.target.value);
  };

  const handleSqlChange = (newValue) => {
    setSqlCode(newValue);
  };

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length === 0) {
      setError('Please upload a valid image file');
      return;
    }

    const uploadedFile = acceptedFiles[0];
    if (!uploadedFile.type.startsWith('image/')) {
      setError('Please upload an image file');
      return;
    }

    setFile(uploadedFile);
    setError(null);

    // Create a preview
    const reader = new FileReader();
    reader.onload = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(uploadedFile);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    },
    maxFiles: 1
  });

  const handleSubmit = async () => {
    if (!file) {
      setError('Please upload an ER diagram image');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('db_engine', dbEngine);

      const response = await axios.post('/api/er-to-sql', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
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
          ER Diagram to SQL
        </Typography>
        <Typography paragraph align="center" color="text.secondary" sx={{ mb: 6 }}>
          Upload an Entity-Relationship diagram image and let our AI convert it to SQL code.
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Upload ER Diagram
              </Typography>
              <Box 
                sx={{ 
                  border: '2px dashed',
                  borderColor: isDragActive ? 'primary.main' : 'grey.400',
                  borderRadius: 1,
                  p: 3,
                  textAlign: 'center',
                  mb: 3,
                  bgcolor: isDragActive ? 'action.hover' : 'background.paper',
                  cursor: 'pointer'
                }}
                {...getRootProps()}
              >
                <input {...getInputProps()} />
                {preview ? (
                  <Box>
                    <img 
                      src={preview} 
                      alt="ER Diagram Preview" 
                      style={{ maxWidth: '100%', maxHeight: '200px', marginBottom: '10px' }} 
                    />
                    <Typography variant="body2">
                      {file?.name} - {Math.round(file?.size / 1024)} KB
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Click or drag to replace
                    </Typography>
                  </Box>
                ) : (
                  <Typography>
                    {isDragActive ? 'Drop the file here' : 'Drag and drop an ER diagram image here, or click to select file'}
                  </Typography>
                )}
              </Box>

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
                  disabled={loading || !file}
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

export default ERToSQL; 