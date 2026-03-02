import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

export default function HelplinesPage() {
  // Mock data for helplines
  const helplines = [
    {
      id: 1,
      name: "PM Kisan Helpline",
      number: "155261",
      description: "Support for farmer welfare schemes",
      hours: "24x7",
      languages: ["Hindi", "English"],
      category: "Agriculture"
    },
    {
      id: 2,
      name: "Ayushman Bharat Helpline",
      number: "14555",
      description: "Health insurance scheme support",
      hours: "9 AM - 6 PM",
      languages: ["Hindi", "English", "Regional"],
      category: "Healthcare"
    },
    {
      id: 3,
      name: "PMAY Helpline",
      number: "1800-11-6446",
      description: "Housing scheme assistance",
      hours: "9 AM - 6 PM",
      languages: ["Hindi", "English"],
      category: "Housing"
    },
    {
      id: 4,
      name: "Women Helpline",
      number: "1091",
      description: "Support for women welfare schemes",
      hours: "24x7",
      languages: ["Hindi", "English", "Regional"],
      category: "Women Welfare"
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Helplines</h1>
        <Button variant="primary">
          Emergency Contact
        </Button>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <h3 className="font-semibold text-blue-900 mb-2">Need Immediate Help?</h3>
        <p className="text-blue-800 mb-3">
          Call our Voice for Bharat support line for assistance with any government scheme.
        </p>
        <div className="flex items-center gap-4">
          <Button variant="primary" size="sm">
            Call 1800-XXX-XXXX
          </Button>
          <Button variant="secondary" size="sm">
            WhatsApp Support
          </Button>
        </div>
      </div>

      <div className="grid gap-4">
        {helplines.map((helpline) => (
          <Card key={helpline.id} className="p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {helpline.name}
                </h3>
                <p className="text-gray-600 mb-3">{helpline.description}</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-blue-600">{helpline.number}</p>
                <p className="text-sm text-gray-500">{helpline.hours}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <p className="text-sm text-gray-500">Category</p>
                <p className="font-medium">{helpline.category}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Languages</p>
                <p className="font-medium">{helpline.languages.join(", ")}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Availability</p>
                <p className="font-medium">{helpline.hours}</p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button variant="primary" size="sm">
                Call Now
              </Button>
              <Button variant="secondary" size="sm">
                Save Contact
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <Card className="p-6 bg-gray-50">
        <h3 className="font-semibold text-gray-900 mb-3">Other Support Channels</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-green-600 font-bold">📱</span>
            </div>
            <h4 className="font-medium mb-1">WhatsApp</h4>
            <p className="text-sm text-gray-600">Chat support available</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-blue-600 font-bold">✉️</span>
            </div>
            <h4 className="font-medium mb-1">Email</h4>
            <p className="text-sm text-gray-600">support@voiceforbharat.in</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-purple-600 font-bold">🎤</span>
            </div>
            <h4 className="font-medium mb-1">Voice Assistant</h4>
            <p className="text-sm text-gray-600">Ask questions anytime</p>
          </div>
        </div>
      </Card>
    </div>
  );
}