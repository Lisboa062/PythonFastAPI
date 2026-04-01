from app.models.models import User


def get_user_by_email(email, session):
    return session.query(User).filter(User.email == email).first()


def create_user(session, user_schema, crypt_password):
        
        new_user = User(
            user_schema.name,
            user_schema.email,
            crypt_password,
            user_schema.active,
            user_schema.admin,
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user