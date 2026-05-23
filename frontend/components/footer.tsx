export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">ResumeParser</h3>
            <p className="text-gray-400 text-sm">
              Professional resume parsing and analysis powered by advanced AI technology.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a
                  href="https://github.com/krish-arya/resume-parser-frontend--1-"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  Documentation
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/krish-arya/resume-parser-frontend--1-/blob/main/readme.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  API Reference
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/krish-arya/resume-parser-frontend--1-/tree/main"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  Releases
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a href="mailto:krisharya2k5@gmail.com" className="hover:text-white transition-colors">
                  Technical Support
                </a>
              </li>
              <li>
                <a href="mailto:krisharya2k5@gmail.com" className="hover:text-white transition-colors">
                  Sales Inquiries
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/your-username/resume-parser/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  Report Issues
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Contact</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <strong className="text-white">Developer 1:</strong>
                <br />
                <a href="mailto:krisharya2k5@gmail.com" className="hover:text-white transition-colors">
                  mvibhuti82@gmail.com
                </a>
              </li>
              <li>
                <strong className="text-white">Developer 2:</strong>
                <br />
                <a href="mailto:kashikamalhotra4@gmail.com" className="hover:text-white transition-colors">
                  kashikamalhotra4@gmail.com
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2024 ResumeParser. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
