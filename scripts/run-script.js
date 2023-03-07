const execa = require('execa');

module.exports = {
  onPreBuild: async ({ inputs }) => {
    try {
      await execa('python', [inputs.scriptPath]);
    } catch (error) {
      console.error(error);
      process.exit(1);
    }
  },
};
