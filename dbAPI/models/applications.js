const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const uuid = require("uuid");

// Create Schema
const ApplicationSchema = new Schema({
  first_name: {
    type: String,
    required: true
  },
  last_name: {
    type: String,
    required: true
  },
  application_uid: {
    type: String,
    default: uuid()
  },
  app_submission_date: {
    type: Date,
    default: Date.now
  },
  region: {
    type: String,
    required: true
  },
  candidate_type: {
    type: String,
    required: true
  },
  process_status: {
    type: String,
    required: Boolean
  },
  academic_year: {
    type: String,
    required: true
  },
  major: {
    type: String,
    required: true
  },
  secondary_major: {
    type: String
  },
  career_interest: {
    type: String,
    required: true
  },
  gpa: {
    type: Number,
    required: true
  },
  college_name: {
    type: String,
    required: true
  },
  phone_number: {
    type: Number,
    required: true
  },
  email: {
    type: String,
    required: true
  }
});

module.exports = Application = mongoose.model("application", ApplicationSchema);
