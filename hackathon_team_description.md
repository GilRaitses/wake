# ORCAST: Immersive Orca Encounter Platform

## Project Overview

ORCAST combines marine science research with real-time environmental data to support orca conservation and improve whale watching experiences. The platform integrates behavioral forecasting, interactive mapping, and AR-guided field viewing to help users plan encounters while contributing sighting data to research.

## What's Already Built and Working

The scientific infrastructure is complete. ORCAST operates as a production system at orcast.org with comprehensive data and ML infrastructure. The backend integrates neuro ethology lab research analyzing kinematic and depth time series from DTAG biologging data with real-time environmental monitoring.

BigQuery data warehouses store DTAG deployments, expert marine biologist annotations, and environmental correlations. Cloud Run services provide real-time behavioral prediction and feeding strategy classification with sub-500ms response times. Firebase manages live sighting reports and environmental data fusion from NOAA sources, historical sightings, and vessel traffic monitoring.

The system classifies feeding strategies from kinematic patterns and integrates environmental feedback from experimental conditions. This enables behavioral forecasting for feeding, traveling, and socializing behaviors while tracking conservation impact.

## The Hackathon Challenge

With robust backend infrastructure operational, the hackathon focuses on creating user-facing experiences that make this scientific platform accessible. The goal is building a working demo by 6pm Day 1.

Day 1 involves creating an Angular application with Material Design connecting to existing orcast.org APIs. Core mapping with Google Maps for probability visualization and basic research analytics with Chart.js. Simple device orientation for AR field-of-view concept demonstration.

Day 2 is demo preparation and final polish only.

## Core Features to Demonstrate

Research Analytics Dashboard shows basic charts of feeding strategy data and environmental correlations from existing APIs. Simple visualization of sighting success metrics across key locations.

Interactive Map displays live probability heatmaps from orcast.org APIs across San Juan Islands with Google Maps integration. Basic historical pattern overlay and viewing location markers.

AR Field Viewer demonstrates concept using device orientation to show directional probability indicators. Simple compass-based interface showing "look here" guidance based on current orca probability data.

## Technical Implementation

Development stack uses Angular with Material Design, Google Maps for mapping with real-time overlays, Chart.js for basic analytics visualization. Simple device orientation API for compass functionality. Direct API connections to orcast.org provide all backend services.

With complete backend infrastructure operational, the team builds proof-of-concept interfaces demonstrating the platform's capabilities in a single day.

## Team Contributions Needed

Frontend developers handle rapid Angular component development and basic Progressive Web App setup. Data visualization specialists create simple charts connecting to existing APIs. Mobile developers integrate basic device orientation for compass demonstration.

UX/UI designers create clean, demo-ready interfaces. Marine science consultants help present data meaningfully and validate the conservation messaging for demos.

## Impact and Applications

The Southern Resident Killer Whale population has declined to 73 individuals. Each encounter provides valuable data contributing to protection efforts. ORCAST enables whale watching trips to contribute to conservation while improving encounter success through scientific prediction, crowdsourced data collection, and real-time conservation education.

This approach helps ensure continued opportunities to observe orcas in their natural habitat while contributing to the science that supports their protection. 