# Adapter: Web App / SaaS / E-commerce

**Enable:** architecture, backend-data, security, design-system if UI.

Determine auth, user roles, entities, schemas, workflows, error states, integrations and production environment. Avoid e-commerce modules the brief does not request: a contact-driven catalog needs no shopping cart or payments.

Test: create/read/update/delete flows as appropriate, access controls, validation, transactions, failures, mobile/desktop UX, external integrations and database migrations.

Separate demonstration content from real data. If admin uploading media/models is requested, include secure upload permissions, quotas, server-side file checks and storage lifecycle.

Do not deploy or migrate production resources without approval.
