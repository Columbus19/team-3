const express = require("express");
const router = express.Router();

// Application Model
const Application = require("../../models/applications");

// @route GET api/applications
// @desc GET All applications
// @access Public
router.get("/", (req, res) => {
  Application.find()
    .sort({ date: -1 })
    .then(applications => res.json(applications));
});

// @route POST api/applications
// @desc Create An Application
// @access Public
router.post("/", (req, res) => {
  const newApplication = new Application({ ...req.body });
  newApplication.save().then(application => res.json(application));
});

// @route Delete api/applications/:id
// @desc Delete An Application
// @access Public
router.delete("/:id", (req, res) => {
  Application.findById(req.params.id)
    .then(application =>
      application.remove().then(() => res.json({ success: true }))
    )
    .catch(err => res.status(404).json({ success: false }));
});

module.exports = router;
