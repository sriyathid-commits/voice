export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-orange to-primary-green">
      <div className="text-center text-white px-6">
        <h1 className="text-4xl md:text-6xl font-bold mb-4">
          Voice for Bharat
        </h1>
        <p className="text-xl md:text-2xl mb-8">
          National Digital Inclusion Project
        </p>
        <p className="text-lg mb-8 max-w-2xl mx-auto">
          Democratizing access to government welfare information across India through multilingual voice interaction
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="/dashboard"
            className="btn-primary px-8 inline-flex items-center justify-center"
          >
            Get Started
          </a>
          <a
            href="/assistant"
            className="btn-secondary px-8 inline-flex items-center justify-center bg-white"
          >
            🎤 Try Voice Assistant
          </a>
        </div>
      </div>
    </main>
  )
}
