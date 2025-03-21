import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
  Container,
} from '@mui/material';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import ImageIcon from '@mui/icons-material/Image';

const Dashboard = () => {
  return (
    <Container>
      <Box sx={{ pt: 4, pb: 8 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
          Transform Your Database Ideas into Reality
        </Typography>
        <Typography variant="h6" paragraph align="center" color="text.secondary" sx={{ mb: 6 }}>
          SmartDB Architect uses AI to convert natural language descriptions and ER diagrams
          into fully functional SQL code. Design, implement, and iterate on database
          schemas with ease.
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <TextFieldsIcon sx={{ fontSize: 60, color: 'primary.main' }} />
                </Box>
                <Typography gutterBottom variant="h5" component="h2" align="center">
                  Natural Language to SQL
                </Typography>
                <Typography align="center">
                  Describe your database in plain English, and let our AI convert it into 
                  optimized SQL code. Perfect for rapid prototyping and iterative development.
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button 
                  variant="contained" 
                  component={RouterLink} 
                  to="/nl-to-sql"
                  size="large"
                >
                  Get Started
                </Button>
              </CardActions>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <ImageIcon sx={{ fontSize: 60, color: 'primary.main' }} />
                </Box>
                <Typography gutterBottom variant="h5" component="h2" align="center">
                  ER Diagram to SQL
                </Typography>
                <Typography align="center">
                  Upload your Entity-Relationship diagrams and convert them directly into SQL code.
                  Our AI extracts entities, attributes, and relationships automatically.
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button 
                  variant="contained" 
                  component={RouterLink} 
                  to="/er-to-sql"
                  size="large"
                >
                  Get Started
                </Button>
              </CardActions>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard; 